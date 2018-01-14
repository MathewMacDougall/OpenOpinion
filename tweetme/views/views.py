from django import http
from tweetme import utils
import twitter
import random
import os

CONSUMER_KEY = "ET6mcjXi8L6RxK5kH2e4zDBCa"
CONSUMER_SECRET = "AhlnBaCBtpxmoYbH4aefITQHYDiCP8Plo0ejqOVrc4NYQiqLDk"
ACCESS_TOKEN = "859835152507125761-M2zMka0P1zYdUbWZTdum3vnMI0IPnzO"
ACCESS_SECRET = "2SyT2qaNGkYWZgXERiBX01lHZU3VnUgVSZWFRwVJ5p1zM"

BATCHES_TWEETS = 1
TOP_N = 10
COUNT = 20

auth = twitter.OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
tweety = twitter.Twitter(auth=auth)

def analyze(request):
    keyword = request.GET.get('keyword')
    type = request.GET['type']
    print("keywords are {} and type is {}".format(keyword, type))

    # The array where we store the results for each keyword
    agg_sent = {}
    weights = {}
    tweets = []

    import time
    t0 = time.time()
    max_id = None
    for i in range(BATCHES_TWEETS):
        # Get the tweet data for each keyword
        res = tweety.search.tweets(q=keyword,lang='en',result_type='recent',count=COUNT, max_id=max_id)
        #return http.JsonResponse(res, safe=False)
        # Extract the important info from the tweets

        for s in res['statuses']:
            # Remove emojies from the text
            text = ''.join([x for x in s['text'] if ord(x) < 256])
            tweets.append({
                'text': text, # The body of the tweet
                'retweet_count': s['retweet_count'], # Retweet count
                'user_followers': s['user']['followers_count'], # User followers
                'created_at': s['created_at'], # Time tweet was created
                'id': s['id'], # Unique id of tweet
                'timestamp': time.time() # Our own timestamp of when this tweet was read
            })
        max_id = min([s['id'] for s in res['statuses']])

    t1 = time.time()
    print(f'Took {t1 - t0}s to fetch {BATCHES_TWEETS} batches of tweets')

    # Load any cached data for this query
    cache_metas = utils.load_cache_file(keyword)
    cache_tweet_ids = {t['id'] for t in cache_metas}

    # Remove any scraped tweets that are already in the cache
    tweets = [t for t in tweets if t['id'] not in cache_tweet_ids]

    tweet_metas = utils.analyze_tweets(tweets)
    print(f'Took {time.time() - t1}s to analyze tweets')

    # Combine cached results and new results. Store this new data in the cache again
    total_tweet_results = cache_metas + tweet_metas
    utils.save_cache_file(keyword, total_tweet_results)
    #return http.JsonResponse(res, safe=False)

    for meta in total_tweet_results:
        for entity in meta['entities']:
            if entity == 'RT': continue
            if entity not in weights:
                weights[entity], agg_sent[entity] = 0, 0
            weights[entity] += 1
            agg_sent[entity] += meta['sentiment']

    max_weight = max([v for v in weights.values()])
    max_sent = max([abs(v) for v in agg_sent.values()])
    for k in weights:
        weights[k] /= max_weight
    for k in agg_sent:
        agg_sent[k] /= max_sent

    results = [{'entity': e, 'weight': weights[e], 'sentiment': agg_sent[e]} for e in weights]
    results.sort(key=lambda r: r['weight'], reverse=True)
    return http.JsonResponse(results[:TOP_N], safe=False)

def fakeanalyze(request):
    fake = [
        {"entity": "Trump",
         "weight": random.random(),
         "sentiment": random.random() * 2 - 1
        },
        {"entity": "cats",
         "weight": random.random(),
         "sentiment": random.random() * 2 - 1
        },
        {"entity": "gucci",
         "weight": random.random(),
         "sentiment": random.random() * 2 - 1
        },
        {"entity": "Justin Trudeau",
         "weight": random.random(),
         "sentiment": random.random() * 2 - 1
        },
        {"entity": "NWHacks",
         "weight": random.random(),
         "sentiment": random.random() * 2 - 1
        }
        ]

    return http.JsonResponse(fake, safe=False)

# Returns the average sentiment for a list of tweets
# def get_sentiment_score(tweets):
#     # Get the sentiment score for each tweet
#     # Use Kai's function call here
#     scores = [get_sentiment(tweet.text) for tweet in tweets]
#     mean_score = np.mean(scores)
#     return mean_score
