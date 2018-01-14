from django import http
import twitter
import numpy as np
import random

CONSUMER_KEY = "ET6mcjXi8L6RxK5kH2e4zDBCa"
CONSUMER_SECRET = "AhlnBaCBtpxmoYbH4aefITQHYDiCP8Plo0ejqOVrc4NYQiqLDk"
ACCESS_TOKEN = "859835152507125761-M2zMka0P1zYdUbWZTdum3vnMI0IPnzO"
ACCESS_SECRET = "2SyT2qaNGkYWZgXERiBX01lHZU3VnUgVSZWFRwVJ5p1zM"

auth = twitter.OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
tweety = twitter.Twitter(auth=auth)

def analyze(request):
    keywords = request.GET['keyword']
    print("keywords are {} and type is {}".format(keywords, type))

    # The array where we store the results for each keyword
    result = []
    sentiment_scores = []
    weights = []

    for keyword in keywords: 
        # Get the tweet data for each keyword
        res = tweety.search.tweets(q=keyword,lang='en',result_type='recent',count=100)

        # Extract the important info from the tweets
        tweets = []
        for s in res['statuses']:
            # Remove emojies from the text
            text = ''.join([x for x in s['text'] if ord(x) < 256])
            tweets.append({
                'text': text,
                'retweet_count': s['retweet_count'],
                'user_followers': s['user']['followers_count'],
                'created_at': s['created_at']
            })

        # Get the sentiment score for this keyword
        sentiment_scores.append(random.random())#get_sentiment_score(tweets))

        # Get the weight for this keyword
        weights.append(get_weight(tweets))

    # Normalize the results before saving to the results
    norm_sentiment = normalize(sentiment_scores)
    norm_weights = normalize(weights)

    for i in range(len(keywords)):
        result.append({
            "entity": keywords[i],
            "weight": norm_weights[i],
            "sentiment": norm_sentiment[i]
            })

    return http.JsonResponse(result, safe=False)

def fakeanalyze(request):
    q = request.GET['user_query']
    print(q)
    fake = [
        {"entity": "Trump",
         "weight": "0.7",
         "sentiment": "-0.7"
        },
        {"entity": "cats",
         "weight": "0.3",
         "sentiment": "0.5"
        },
        {"entity": "gucci",
         "weight": "0.05",
         "sentiment": "0.1"
        },
        {"entity": "Justin Trudeau",
         "weight": "0.97",
         "sentiment": "0.99"
        },
        {"entity": "NWHacks",
         "weight": "0.5",
         "sentiment": "0.6"
        }
        ]

    return http.JsonResponse(fake, safe=False)

# Returns the average sentiment for a list of tweets
def get_sentiment_score(tweets): 
    # Get the sentiment score for each tweet
    # Use Kai's function call here
    scores = [get_sentiment(tweet.text) for tweet in tweets]
    mean_score = np.mean(scores)
    return mean_score

# Returns the weight for the keyword for a list of tweets
def get_weight(tweets):
   return 0.5 

# Normalizes the values in an array
def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
       return v
    return v / norm
