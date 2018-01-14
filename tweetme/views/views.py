from django import http
import twitter

CONSUMER_KEY = "ET6mcjXi8L6RxK5kH2e4zDBCa"
CONSUMER_SECRET = "AhlnBaCBtpxmoYbH4aefITQHYDiCP8Plo0ejqOVrc4NYQiqLDk"
ACCESS_TOKEN = "859835152507125761-M2zMka0P1zYdUbWZTdum3vnMI0IPnzO"
ACCESS_SECRET = "2SyT2qaNGkYWZgXERiBX01lHZU3VnUgVSZWFRwVJ5p1zM"

auth = twitter.OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
tweety = twitter.Twitter(auth=auth)

def analyze(request):
    q = request.GET['user_query']


    res = tweety.search.tweets(q=q)

    # Do crazy NLP stuff
    entities = [{"entity": "Donald Trump", "mentions": 1207, "sentiment_sum": -23321.3},
                {"entity": "Barack Obama", "mentions": 455, "sentiment_sum": 4211.3},
                {"entity": "Hilary Clinton", "mentions": 551, "sentiment_sum": -100},
                {"entity": q, "mentions": 12007, "sentiment_sum": 99999}]

    entities = [t.get('text') for t in res['statuses']]
    import pprint
    pprint.pprint(entities)
    pprint.pprint(res['statuses'][0])


    entities = []
    for s in res['statuses']:
        text = s['text'].replace('\\u[0-9a-f]{4}', '')
        entities.append({
            'text': text,
            'retweet_count': s['retweet_count'],
            'user_followers': s['user']['followers_count']
        })

    return http.JsonResponse(entities, safe=False)