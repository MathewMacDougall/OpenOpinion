import requests

NLP_SERVICE_URL = 'localhost:9000/?properties={"annotators":"tokenize,ssplit,parse,pos,sentiment,","outputFormat":"json"}'

def analyze_tweet(tweets):
    tweets = [t.replace('\.', ',') for t in tweets]
    tweet_block = '. '.join(tweets) + '.'
    res = requests.post(NLP_SERVICE_URL, data=tweet_block).json()
    data = res['sentences']

    nouns = []
    sentenceSentimentScore = []

    for sentence in data:
        words = str(sentence['parse']).split()
        if '(NNP' in words:
            noun = words[words.index('(NNP') + 1:[words.index(x) for x in words if x.endswith('))')][0] + 1]
            if '(NNP' in noun:
                noun.remove('(NNP')
            noun = ' '.join(noun).replace(')', '')
            nouns.append(noun)

        sentenceSentimentScore.append(int(sentence['sentimentValue']) * (sentence['sentiment'] == 'Negative' and -1 or 1))

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

