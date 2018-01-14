import requests

NLP_SERVICE_URL = 'http://localhost:9000/?properties={"annotators":"tokenize,ssplit,pos,lemma,ner,parse,dcoref,sentiment,depparse,natlog,openie","outputFormat":"json"}'

def analyze_tweets(tweets):
    tweets = [t.replace('\.', ',') for t in tweets]
    tweet_block = '. '.join(tweets) + '.'
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

    for sentence in data:
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

        tweet_metas.append({'sentiment': sent, 'entities': entities})

    return tweet_metas
