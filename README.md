# Twitter-API 
Uses the Twitter Streaming API to track a given keyword and generate various reports about the tweets.
After starting program prints the following reports based on the tweets of last 5 minutes.
1. User Report
2. Links Report
3. Content Report

## Dependency
- Install Tweepy (Wrapper to Twitter API)
- Install NLTK 
	(To remove stop words. Can be ignored if we generate stop words once and cache it)
- Install tld (To extract domain names from URLs)

## Execution

python tw_threaded.py [KEYWORD 1] [KEYWORD 2] ... [KEYWORD n]
