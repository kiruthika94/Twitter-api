# raw program without threads and usable output

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from twython import Twython, TwythonError
import nltk

from nltk.corpus import stopwords
from tld import get_tld
from tld.utils import update_tld_names
import  time
import tweepy
import json
from ttp import ttp
from collections import Counter
import re
import httplib
import urlparse
import pprint
import string
import sys



#update_tld_names()

access_token = "3256307588-uMzXrpibNi3pcMrhNTado6MZLrLWVblzChDUMds"
access_token_secret = "VtxmJBmp30T7vtCwacmN1MoqYTctUafxRjnAvQyxJNYEz"
consumer_key = "p3np2dQzMiVfVpjhN900zT3DV"
consumer_secret = "K2hWAGrs2sMWmOLfHpNfFSFV70L9wwimJMpxbF8Bk7GCBO83pM"

class StdOutListener(StreamListener):
    def on_data(self,data):
        pprint.pprint(json.loads(data))
	exit()
        #with open('twitter_data.txt','a') as tf:
        #    tf.write(data)
        #return True

    def on_error(self,status):
        print status

def expand_url(url):
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




if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    cli_args = sys.argv
    cli_args.pop(0)
    stream.filter(track=cli_args)

    exit()


    

    tweets_data_path = '/vagrant/web/twitter_data.txt'
    domain = []
    domain_data = []
    domain_names =[]
    domain_count = []
    myurls =[]
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
    for url in urls:
        myurls.append(expand_url(url))
        for url in myurls:
            domain_data = get_tld(url, as_object=True)
            if not domain_data.subdomain:
                domain = domain_data.tld
            else:
                domain = "{}.{}".format(domain_data.subdomain, domain_data.tld)
            domain_names.append(domain)
    domain_count=Counter(domain_names)
    #print domain_count , myurls
    
    
 

    mytext= []
    texts = [tweet['text'] for tweet in tweets_data]
    for line in texts:
        
        line =' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",line).split())
        mytext.append(line)
 
    terms_stop = []
    punctuation = list(string.punctuation)
    stop = stopwords.words('english') + punctuation + ['rt', 'via']
    terms_stop = [word for word in mytext if word not in stop and not  word.startswith(('#', '@'))]
    pprint.pprint(terms_stop)
    
    
