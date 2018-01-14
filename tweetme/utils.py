import itertools
import requests
import os
import json
import time
import threading

NLP_SERVICE_URL = 'http://localhost:9000/?properties={"annotators":"tokenize,ssplit,pos,lemma,ner,parse,dcoref,sentiment,depparse,natlog,openie","outputFormat":"json"}'
CACHE_PATH = "cache/"
CACHE_TIME = 60 * 60 # 1 hour
NUM_THREADS = 10

def process_block(tweet_block, results, i):
    res = requests.post(NLP_SERVICE_URL, data=tweet_block)
    res = res.json()
    results[i] = res['sentences']

def analyze_tweets(tweets, just_sentiment=False):
    tweets_text = [t['text'] for t in tweets]
    tweets_text = [t.replace('.', ',') for t in tweets_text]
    chunk_size = len(tweets_text) // NUM_THREADS
    threads = []
    results = [] * NUM_THREADS
    for i in range(NUM_THREADS):
        tweet_chunk = tweets_text[i*chunk_size:(i+1)*chunk_size]
        if i + 1 == NUM_THREADS:
            tweet_chunk += tweets_text[(i+1)*chunk_size:(i+2)*chunk_size]
        tweet_block = '. '.join(tweet_chunk) + '.'
        thread = threading.Thread(target=process_block, args=(tweet_block, results, i))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    data = list(itertools.chain.from_iterable(results))
    tweet_metas = []
    print("len data is {}, len tweets is {}".format(len(data), len(tweets)))

    for i in range(min(len(data), len(tweets))):
        sentence = data[i]

        sentiment = int(sentence['sentimentValue']) * (sentence['sentiment'] == 'Negative' and -1 or 1)

        if not just_sentiment:
            tokens = filter(lambda word: str(word['pos']).startswith('NN'), sentence['tokens'])
            tokens = [token['word'] for token in tokens]

            compounds = set()
            for structure in sentence['openie']:
                compounds.add(structure['subject'])
                compounds.add(structure['object'])
            aggregate = ' '.join(compounds) # TODO: I've commited a grave sin.

            entities = [word for word in tokens if word not in aggregate]
            entities.extend(list(compounds))
            tweet_metas.append({'sentiment': sentiment, 'entities': entities, 'id': tweets[i]['id'],
                                'timestamp': tweets[i]['timestamp']})
        else:
            tweet_metas.append({'sentiment': sentiment, 'id': tweets[i]['id'],
                                'timestamp': tweets[i]['timestamp']})


    return tweet_metas

def load_cache_file(query):
    filename = CACHE_PATH + get_cache_filename(query)
    result = []
    if os.path.isfile(filename):
        with open(filename, 'r') as file:
            result = json.load(file)

        ct = time.time()
        result = [r for r in result if r['timestamp'] - ct <= CACHE_TIME]
    return result

def save_cache_file(query, nlp_data):
    filename = CACHE_PATH + get_cache_filename(query)
    with open(filename, 'w') as file:
        json.dump(nlp_data, file)

def get_cache_filename(query):
    return query.replace(" ", "_") + ".json"

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)
