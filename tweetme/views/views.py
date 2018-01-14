from django import http
from tweetme import utils
import twitter
import random
import re

CONSUMER_KEY = "ET6mcjXi8L6RxK5kH2e4zDBCa"
CONSUMER_SECRET = "AhlnBaCBtpxmoYbH4aefITQHYDiCP8Plo0ejqOVrc4NYQiqLDk"
ACCESS_TOKEN = "859835152507125761-M2zMka0P1zYdUbWZTdum3vnMI0IPnzO"
ACCESS_SECRET = "2SyT2qaNGkYWZgXERiBX01lHZU3VnUgVSZWFRwVJ5p1zM"

BATCHES_TWEETS = 1 # How many times to fetch tweets per keyword
TOP_N = 10 # How many assicociated words to return
COUNT = 50 # How many tweets to retrieve per query (MAX is 100)
SMALL_COUNT = 10 # How many tweets to retrieve per query (MAX is 100)

auth = twitter.OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
tweety = twitter.Twitter(auth=auth)

SKIP_ENTITIES = ['rt']

def analyze(request):
    print("\n\n")
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
            text = re.sub(r'RT ', '', text)
            # text = re.sub(r'RT @?(\w){1,15}:', '', text)
            text = re.sub(r'(?:(?:https?|ftp):\/\/)(?:\S+(?::\S*)?@)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,}))\.?)(?::\d{2,5})?(?:[/?#]\S*)?', '', text)
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
    print(f'Took {t1 - t0}s to fetch {BATCHES_TWEETS*COUNT} tweets')

    # Load any cached data for this query
    cache_metas = utils.load_cache_file(keyword)
    cache_tweet_ids = {t['id'] for t in cache_metas}

    # Remove any scraped tweets that are already in the cache
    tweets = [t for t in tweets if t['id'] not in cache_tweet_ids]

    t2 = time.time()
    tweet_metas = utils.analyze_tweets(tweets)
    t3 = time.time()
    print(f'Loaded {len(cache_metas)} results from cache')
    print(f'Took {t3 - t2}s to analyze {len(tweet_metas)} new tweets')

    # Combine cached results and new results. Store this new data in the cache again
    total_tweet_results = cache_metas + tweet_metas
    utils.save_cache_file(keyword, total_tweet_results)

    for meta in total_tweet_results:
        for entity in meta['entities']:
            if entity.lower() in SKIP_ENTITIES: continue
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

def analyze_many(request):
    print("\n\n")
    keywords = request.GET.get('keywords').split(',')
    type = request.GET['type']
    print("keywords are {} and type is {}".format(keywords, type))

    # The array where we store the results for each keyword
    agg_sent = {}
    weights = {}
    tweet_metas = []

    import time
    t0 = time.time()
    max_id = None
    for keyword in keywords:
	print(f'Current keyword is {keyword}')
        # Get the tweet data for each keyword
        tweets_for_kw = []
        res = tweety.search.tweets(q=keyword,lang='en',result_type='recent',count=SMALL_COUNT, max_id=max_id)
        #return http.JsonResponse(res, safe=False)
        # Extract the important info from the tweets

        for s in res['statuses']:
            # Remove emojies from the text
            text = ''.join([x for x in s['text'] if ord(x) < 256])
            text = re.sub(r'RT ', '', text)
            # text = re.sub(r'RT @?(\w){1,15}:', '', text)
            text = re.sub(r'(?:(?:https?|ftp):\/\/)(?:\S+(?::\S*)?@)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,}))\.?)(?::\d{2,5})?(?:[/?#]\S*)?', '', text)
            tweets_for_kw.append({
                'text': text, # The body of the tweet
                'retweet_count': s['retweet_count'], # Retweet count
                'user_followers': s['user']['followers_count'], # User followers
                'created_at': s['created_at'], # Time tweet was created
                'id': s['id'], # Unique id of tweet
                'timestamp': time.time() # Our own timestamp of when this tweet was read
            })
        max_id = min([s['id'] for s in res['statuses']])

        t1 = time.time()
        print(f'Took {t1 - t0}s to fetch {SMALL_COUNT} tweets')

        # Load any cached data for this query
        cache_metas = utils.load_cache_file(keyword)
        cache_tweet_ids = {t['id'] for t in cache_metas}

        # Remove any scraped tweets that are already in the cache
        tweets_for_kw = [t for t in tweets_for_kw if t['id'] not in cache_tweet_ids]

        t2 = time.time()
        tweet_metas = utils.analyze_tweets(tweets_for_kw)
        t3 = time.time()
        print(f'Loaded {len(cache_metas)} results from cache')
        print(f'Took {t3 - t2}s to analyze {len(tweet_metas)} new tweets')

        # Combine cached results and new results. Store this new data in the cache again
        total_tweet_results = cache_metas + tweet_metas
        utils.save_cache_file(keyword, total_tweet_results)

        for t in total_tweet_results:
            t['entitity'] = keyword

        tweet_metas += total_tweet_results

    for meta in tweet_metas:
        for entity in meta['entities']:
            if entity.lower() in SKIP_ENTITIES: continue
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
    return http.JsonResponse(results, safe=False)


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
