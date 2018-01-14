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

    entities = []
    for s in res['statuses']:
        text = ''.join([x for x in s['text'] if ord(x) < 256])
        entities.append({
            'text': text,
            'retweet_count': s['retweet_count'],
            'user_followers': s['user']['followers_count']
        })

    return http.JsonResponse(entities, safe=False)