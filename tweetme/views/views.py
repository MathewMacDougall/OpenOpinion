from django import http

def analyze(request):
    q = request.GET['user_query']

    # Do crazy NLP stuff
    entities = [{"entity": "Donald Trump", "mentions": 1207, "sentiment_sum": -23321.3},
                {"entity": "Barack Obama", "mentions": 455, "sentiment_sum": 4211.3},
                {"entity": "Hilary Clinton", "mentions": 551, "sentiment_sum": -100},
                {"entity": q, "mentions": 12007, "sentiment_sum": 99999}]

    return http.JsonResponse(entities, safe=False)