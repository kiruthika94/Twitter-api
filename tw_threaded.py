#!/usr/bin/python
print "Initializing Libraries..."
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from nltk.corpus import stopwords
from tld import get_tld
#from tld.utils import update_tld_names
import json
from collections import Counter
import re
import httplib
import urlparse
#import pprint
import thread
import time
import sys
import string

processed_tweets = {}
cachedStopWords = stopwords.words("english")
cli_args = []

class StdOutListener(StreamListener):
    def on_data(self, data):
    	global processed_tweets
    	data_json = json.loads(data)
    	#pprint.pprint(data_json)
    	processed_tweet = {}
    	processed_tweet['tweet'] = data_json['text']
    	processed_tweet['username'] = data_json['user']['screen_name']
    	processed_tweet['timestamp'] = time.time()
    	urls = []
    	for url in data_json['entities']['urls']:
    		expanded_url = ExpandUrl(url['expanded_url'])
    		urls.append(expanded_url)
    	processed_tweet['urls'] = urls
        processed_tweets[data_json['id']] = processed_tweet
        #with open('twitter_data.txt','a') as tf:
        #    tf.write(data)
        #return True

    def on_error(self, status):
        print status

def ExpandUrl(url):
    parsed = urlparse.urlparse(url)
    h = httplib.HTTPConnection(parsed.netloc)
    resource = parsed.path
    if parsed.query != "":
        resource += "?" + parsed.query
    h.request('HEAD', resource )
    response = h.getresponse()
    if response.status/100 == 3 and response.getheader('Location'):
        return response.getheader('Location')
    else:
        return url

def GetTweets(threadName, delay):
	global cli_args
	access_token = "3256307588-uMzXrpibNi3pcMrhNTado6MZLrLWVblzChDUMds"
	access_token_secret = "VtxmJBmp30T7vtCwacmN1MoqYTctUafxRjnAvQyxJNYEz"
	consumer_key = "p3np2dQzMiVfVpjhN900zT3DV"
	consumer_secret = "K2hWAGrs2sMWmOLfHpNfFSFV70L9wwimJMpxbF8Bk7GCBO83pM"
	l = StdOutListener()
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	stream = Stream(auth, l)
	cli_args = sys.argv
	cli_args.pop(0)
	try:
		stream.filter(track=cli_args)
	except:
		print "Error in connecting to twitter"
		thread.interrupt_main()
	time.sleep(delay)

def OneMinuteStats(threadName, delay):
	from texttable import Texttable
	global processed_tweets
	print "Script Inititalized."
	while 1:
		time.sleep(delay) # sleep first so that we don't print stats before collecting them.
		# work with copy to prevent RuntimeError: dictionary changed size during iteration
		processed_tweets_copy = {k:v for k,v in processed_tweets.items()}
		now = time.time()
		five_min_ago = now - (5 * 60)
		username_count = Counter()
		total_username = 0
		domain_count = Counter()
		total_links = 0
		word_count = Counter()
		total_words = 0
		for tweet_id, tweet_data in processed_tweets_copy.iteritems():
			if int(tweet_data['timestamp']) < five_min_ago:
				processed_tweets.pop(tweet_id, None)
			else:
				username_count[tweet_data['username']] += 1
				total_username += 1
				for url in tweet_data['urls']:
					total_links += 1
					try:
						domain_data = get_tld(url, as_object=True)
					except:
						continue
					if not domain_data.subdomain:
						domain = domain_data.tld
					else:
						domain = "{}.{}".format(domain_data.subdomain, domain_data.tld)
					domain_count[domain] += 1
				tweet_text = tweet_data['tweet']
				tweet_text = ''.join(ch for ch in tweet_text if ch not in set(string.punctuation))
				tweet_text = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', tweet_text) # remove url http://stackoverflow.com/a/83378
				tweet_text_filtered = [word for word in tweet_text.split() if word.lower() not in cachedStopWords]

				for word in tweet_text_filtered:
					word_count[word] += 1
					total_words += 1

		username_table = Texttable()
		username_table.set_deco(Texttable.HEADER)
		username_table.set_cols_dtype(['t',  'i'])
		username_table.set_cols_align(["l", "r"])
		username_table.header(['Username', 'Tweets'])
		for item in [x[0] for x in username_count.most_common()]:
			username_table.add_row([item.encode('utf-8'), username_count[item]])

		domain_table = Texttable()
		domain_table.set_deco(Texttable.HEADER)
		domain_table.set_cols_dtype(['t',  'i'])
		domain_table.set_cols_align(["l", "r"])
		domain_table.header(['Domain', 'Occurences'])
		for item in [x[0] for x in domain_count.most_common()]:
			domain_table.add_row([item.encode('utf-8'), domain_count[item]])
		
		word_table = Texttable()
		word_table.set_deco(Texttable.HEADER)
		word_table.set_cols_dtype(['t',  'i'])
		word_table.set_cols_align(["l", "r"])
		word_table.header(['Word', 'Occurences'])

		for item in [x[0] for x in word_count.most_common(10)]:
			word_table.add_row([item.encode('utf-8'), word_count[item]])
		
		print "Report at {} for {}".format(time.strftime("%Y-%m-%d %H:%M"), ', '.join(cli_args))
		if total_username:
			print "User Report: "
			print username_table.draw()
			print ""
		if total_links:
			print "Links Report: "
			print "Total Links: {}".format(total_links)
			print domain_table.draw()
			print ""
		if total_words:
			print "Content Report: "
			print word_table.draw()
			print ""
		if total_words or total_links or total_username:
			print "=============================="
		else:
			print "No data for past 5 minutes (or from when the script was started)."

		

try:
	thread.start_new_thread(GetTweets, ("GetTweets", 1 ))
	thread.start_new_thread(OneMinuteStats, ("OneMinuteStats", 60 ))
except:
	print "Error: unable to start thread or a thread failed"

while 1:
	pass
