from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from twython import Twython, TwythonError
import  time
import tweepy
import json
from ttp import ttp
from collections import Counter
import re
import httplib
import urlparse
import pprint




access_token = "3256307588-uMzXrpibNi3pcMrhNTado6MZLrLWVblzChDUMds"
access_token_secret = "VtxmJBmp30T7vtCwacmN1MoqYTctUafxRjnAvQyxJNYEz"
consumer_key = "p3np2dQzMiVfVpjhN900zT3DV"
consumer_secret = "K2hWAGrs2sMWmOLfHpNfFSFV70L9wwimJMpxbF8Bk7GCBO83pM"

class StdOutListener(StreamListener):
    def on_data(self,data):
        #print data
        with open('twitter_data.txt','a') as tf:
            tf.write(data)
        return True

    def on_error(self,status):
        print status

def expand_url(url):
    url_components = urlparse.urlparse(url)
    h = httplib.HTTPConnection(url_components.netloc)
    h.request('HEAD', url_components.path)
    response = h.getresponse()
    if response.status/100 == 3 and response.getheader('Location'):
        return unshorten_url(response.getheader('Location'))
    else:
        return url    



if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    #l = StdOutListener()
    #auth = OAuthHandler(consumer_key, consumer_secret)
    #auth.set_access_token(access_token, access_token_secret)
    #stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    #stream.filter(track=['python', 'javascript', 'ruby'])
    #api = tweepy.API(auth)
    #names=[]
    #for user in tweepy.Cursor(api.followers, screen_name="twitter").items():
     #   names.append(user.screen_name)

   


    

    tweets_data_path = '/vagrant/web/twitter_data.txt'

    tweets_data = []
    tweets_file = open(tweets_data_path, "r")
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            tweets_data.append(tweet)
        except:
            continue

    for tweet in tweets_data:
        urls=re.findall(r'(https?://\S+)', tweet['text'])
    
     print expand_url(urls)
    exit()
    for tweet in tweets_data:
        if tweet['entities']['urls']:
            urls= [tweet['entities']['urls'] for tweet in tweets_data]
            break
    

    urls1 = [(T['entities']['urls'][0]['expanded_url'] if len(T['entities']['urls']) >= 1 else None) for T in tweets_data]
    urls2 = [(T['entities']['urls'][1]['expanded_url'] if len(T['entities']['urls']) >= 2 else None) for T in tweets_data]
    urls1 = filter(None, urls1)

    #times = [tweet['created_at'] for tweet in tweets_data
    #names = [tweet['user']['name'] for tweet in tweets_data]

    count= Counter()
    d=Counter(urls1)
    #screen_names = [tweet['user']['screen_name'] for tweet in 
