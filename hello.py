import flask 
import tweepy
from textblob import TextBlob


consumer_key = "0sQrCsizjYSgWvyJiyyo0q3bi"
consumer_secret = "WCHApm99Bs4RcsBTAaBB0kcjaTryqt0NUPlw1q4W0zuSYHJxs6"
access_token = '2251223796-KRiDAr80PcIdvkJ95KrEocLl4JYs5w3w18F1hAq'
access_token_secret ='MA7Bz64cKZgCV1Fj44inBHPmzmcdYE5cW5S62Ghnw5fBY'
auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth)

def getTweets(key):
	searchFor = str(key)
	public_tweets = api.search(searchFor)
	tweets = []	
	for tweet in public_tweets:
		tweets.append(tweet.text)
	return tweets

def analyzeTweets(tweets):

	positive = []
	negative = []

	for tweet in tweets:

	 	if TextBlob(tweet).sentiment.polarity > 0:
	 		positive.append(tweet)
	 	else:
	 		negative.append(tweet)

	return (len(positive),len(negative))
	
		

app = flask.Flask(__name__)

@app.route('/')
def hello():

	#defaults
	searchFor = 'trump'

	tweets = getTweets(searchFor)


	return flask.render_template('greet_view.html', keyword = searchFor,your_list=tweets)

@app.route('/', methods=['POST'])
def my_form_post():

    text = flask.request.form['text']

    searchFor = text

    tweets = getTweets(searchFor)

    sentiment = analyzeTweets(tweets)

    return flask.render_template('hello_view.html', keyword = searchFor,your_list=tweets, positive = sentiment[0], negative=sentiment[1])

if __name__ == '__main__':
	app.run()