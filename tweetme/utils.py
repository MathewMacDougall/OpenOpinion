import requests

NLP_SERVICE_URL = 'localhost:9000/?properties={"annotators":"tokenize,ssplit,parse,pos,sentiment,","outputFormat":"json"}'

def analyze_tweet(tweets, just_sentiment=False):
    tweets = [t.replace('\.', ',') for t in tweets]
    tweet_block = '. '.join(tweets) + '.'
    res = requests.post(NLP_SERVICE_URL, data=tweet_block).json()
    data = res['sentences']

    tweet_metas = []

    for sentence in data:
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
            tweet_metas.append({'sentiment': sentiment, 'entities': entities})
        else:
            tweet_metas.append({'sentiment': sentiment})

    return tweet_metas
