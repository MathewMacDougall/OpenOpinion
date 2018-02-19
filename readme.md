# Open Opinion
### See how the Twitterverse is currently feeling about various topics

Open Opinion was a project for NWHacks 2018. The idea was to show the general sentiment of recent Tweets about various user-selected topics, as well as the relative popularity of each topic.

### How it works
The user is able to enter keywords, which will cause a new "bubble" to appear for that keyword. The bubbles are sized based on recent tweet activity of each keyword (with larger bubbles corresponding to relatively more activity), and are colored based on the average sentiments of the tweets corresponding to that keyword. In our examples, blue is positive, red is negative.

We use the Twitter API to fetch based on the given keywords, and then run the tweets through Stanford's CoreNLP library to get an "emotion score" for each tweet. These are averaged for each keyword and then translated into the corresponding color.

We calculate the "activity" of each keyword by dividing the total number of tweets we pull by the time between the first and last tweet, to get a measure of "tweets per second". This activity score for each keyword is normalized before being used to create the bubble chart.

Because the CoreNLP library take a relatively long time to run, we cache the results for each tweet to avoid having to run the same NLP again in the future. We are also careful to avoid retrieving previously analyzed tweets when fetching new tweets to minimize the amount of analysis we have to do each time.

##### Setup
1. Download Stanford's CoreNLP library from [here](nfvnqZdo2twVd9dHDnsz2ZibybOWY87CE2esCbdY14pb6). Extract and run it with `java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer - -port 9000 -timeout 15000`
2. Install the Python requirements and run the app with `python manage.py runserver 8000` or something similar
3. Load the static webpage, and enjoy!


