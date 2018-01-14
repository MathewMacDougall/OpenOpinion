import requests

NLP_SERVICE_URL = 'localhost:9000/?properties={"annotators":"tokenize,ssplit,parse,pos,sentiment,","outputFormat":"json"}'

def analyze_tweet(tweets):
    tweets = [t.replace('\.', ',') for t in tweets]
    tweet_block = '. '.join(tweets) + '.'
    res = requests.post(NLP_SERVICE_URL, data=tweet_block).json()
    data = res['sentences']

    tweet_metas = []

    for sentence in data:
        tokens = filter(lambda word: str(word['pos']).startswith('NN'), sentence['tokens'])
        tokens = [token['word'] for token in tokens]

        compounds = set()
        for structure in sentence['openie']:
            compounds.add(structure['subject'])
            compounds.add(structure['object'])
        aggregate = ' '.join(compounds) # TODO: I've commited a grave sin.

<<<<<<< HEAD
        entities = [word for word in tokens if word not in aggregate]
        entities.extend(list(compounds))

        sent = int(sentence['sentimentValue']) * (sentence['sentiment'] == 'Negative' and -1 or 1)

        tweet_metas.append({'sentiment': sent, 'entities': entities})

    return tweet_metas
=======
    return sentenceSentimentScore

def get_top_n_entities(analyzed_tweets, n):


# Returns the weight for the keyword for a list of tweets
def get_weight(tweets):
   return 0.5 

# Normalizes the values in an array
def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
       return v
    return v / norm

>>>>>>> eff279b52aebbf384e35adf0d462a757e1d93a4a
