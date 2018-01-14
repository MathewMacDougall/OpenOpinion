import requests
import os
import json
import time

NLP_SERVICE_URL = 'http://localhost:9000/?properties={"annotators":"tokenize,ssplit,pos,lemma,ner,parse,dcoref,sentiment,depparse,natlog,openie","outputFormat":"json"}'
CACHE_PATH = "cache/"
CACHE_TIME = 60 * 60 # 1 hour

def analyze_tweets(tweets):
    if not tweets:
        return []
    tweets_text = [t['text'] for t in tweets]
    tweets_text = [t.replace('.', ',') for t in tweets_text]
    tweet_block = '. '.join(tweets_text) + '.'
    res = requests.post(NLP_SERVICE_URL, data=tweet_block)
    try:
        raw = res.text
        print(f'{raw[:20]}...{raw[-20:]}')
        res = res.json()
    except BaseException as e:
        print(e)
        print(res.text)
    data = res['sentences']

    tweet_metas = []
    print("len data is {}, len tweets is {}".format(len(data), len(tweets)))

    for i in range(min(len(data), len(tweets))):
        sentence = data[i]
        tokens = filter(lambda word: str(word['pos']).startswith('NN'), sentence['tokens'])
        tokens = [token['word'] for token in tokens]

        compounds = set()
        for structure in sentence['openie']:
            compounds.add(structure['subject'])
            compounds.add(structure['object'])
        aggregate = ' '.join(compounds) # TODO: I've commited a grave sin.

        entities = [word for word in tokens if word not in aggregate]
        entities.extend(list(compounds))

        sent = int(sentence['sentimentValue']) * (sentence['sentiment'] == 'Negative' and -1 or 1)

        tweet_metas.append({'sentiment': sent, 'entities': entities, 'id': tweets[i]['id'],
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