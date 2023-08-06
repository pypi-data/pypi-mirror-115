# Tweet Scraping

## Prerequisites

1. Internet Connection
2. Python 3.6+
3. Must have present credentials (i,e: consumer key, consumer secret, access token, access token secret) by creating an account on Twitter Dev
4. The code will create the output in the form of a csv file at the location of same code
5. The dataset created will be unique at tweetid level

## Installing Tweet Scraping

```sh
pip3 install tweetScraping
```

## Using tweetScraping

Just import tweetScraping and call functions!

## Code Usage:

```sh
import tweetScraping
a = tweetScraping.tweetScraping(consumer_key : str ,  consumer_secret :str, access_token : str , access_token_secret : str, query : str , [file_name:str],[no_of_tweets : int])
a.start()
```

## Code Example:
## NOTE: These are dummy keys and tokens and are only for representation, please replace these with your credentials
```sh
import tweetScraping
a = tweetScraping.tweetScraping('ghF98tufKbgWpGxHVbBTkx9L5' ,
                                'EiyUJ9aEdwTEKEe2HLuo8ZhBTJscztgaEpSBY38YZhSUkq1Az4',
                                '1099325182525661186-9dn78kOA4Z09plZWPHrn9nmgdukg6j',
                                'dZMfqR9O4eCQLvS0bnWNYr9eivjS4wtwsPY8WnBugR5xJ',
                                'GOT',
                                1000)
a.start()
```
## This will output a csv file by the name GOT.csv, with 1000 tweets, this 1000 tweets can be increased further

## Description of 33 columns created in the form of structured data from twitter unstructured data

```sh
1) tweet_id: the tweet id prefized and suffixed by '~' so that no digits are lost
2) tweet_created_at: When was the tweet posted on Twitter
3) tweet_created_on_holiday_bool: A boolean to tell if the tweet was posted on a 
national holiday or not(True:Yes, False: No)
4) tweet_created_on_weekend_bool: A boolean to tell if the tweet was posted on a 
weekend or not(True:Yes, False: No)
5) tweet_created_at_noon_bool: A boolean to tell if the tweet was posted during 
noon hours or not(True:Yes, False: No)
5) tweet_created_at_eve_bool: A boolean to tell if the tweet was posted during 
evening hours or not(True:Yes, False: No)
6) user_id: Twitter user account from which the tweet was posted prefixed and 
suffixed by '~' so that no integer is lost
7) user_screen_name: Twitter user screen name from which the tweet was posted, 
will have actual case(If it is camel case it remains as is)
8) user_screen_name_length: Length of the Twitter user screen name from which 
the current tweet was posted
9) user_no_of_tweets: How many tweets have been posted from the screen name 
since date of creation of account till the date this code getting executed
10) user_no_of_followers: Number of followers of the Twitter user screen name 
from which the current tweet was posted
11) user_no_of_followings: Number of accounts the Twitter user screen name 
follow from which the current tweet was posted
12) user_account_age: How old the Twitter user account on Twitter is from 
which the current tweet was posted (current date - account creation date)
13) user_no_of_favourites: Number of tweets liked by the Twitter 
user screen name from which the current tweet was posted
14) user_average_tweets: On a daily basis, how many tweets the Twitter 
user screen name post from which the current tweet was posted
15) user_average_favourites: On a daily basis, how many tweets the Twitter 
user screen name like from which the current tweet was posted
16) user_account_location: The geographical location(if shared) the Twitter 
user screen name from which the current tweet was posted
17) tweet_text: Tweet text post cleaning 
(cleaning done for (@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+), 
and case standardization)
18) tweet_text_length: Length of the tweet text post cleaning
19) tweet_text_optimal_length: A boolean to tell if the tweet posted was of 
optimal length or less prior to cleaning(True:Yes, False: No)
20) tweet_text_no_of_hashtags: How many hashtags were present in the original 
tweet text before cleaning the text
21) tweet_text_contains_hashtags: A boolean to tell if the tweet posted had a 
hashtag or not prior to cleaning(True:Yes, False: No)
22) tweet_text_contains_url: A boolean to tell if the tweet posted had any url 
embedded prior to cleaning(True:Yes, False: No)
23) tweet_text_no_of_user_mentions: How many other screen names were tagged in 
the tweet text using '@'
24) tweet_text_contains_user_mentions: A boolean to tell if the tweet posted had
any user mentions prior to cleaning(True:Yes, False: No)
25) tweet_text_sentiment: The sentiment of the tweet
26) tweet_text_contains_media: A boolean to tell if the tweet posted had any 
multimedia prior to cleaning(True:Yes, False: No)
27) tweet_text_contains_number: A boolean to tell if the tweet posted had any 
numbers prior to cleaning(True:Yes, False: No)
28) tweet_text_contains_upper_words: A boolean to tell if the tweet posted had 
upper case words to emphasize the meaning prior to cleaning(True:Yes, False: No)
29) tweet_text_contains_lower_words: A boolean to tell if the tweet posted had 
lower case words prior to cleaning(True:Yes, False: No)
30) tweet_text_contains_excl: A boolean to tell if the tweet posted had 
exclamations prior to cleaning(True:Yes, False: No)
31) tweet_text_contains_retweet_suggestion: A boolean to tell if the tweet 
posted had 'RT' asking to retweet prior to cleaning(True:Yes, False: No)
32) retweeted: A boolean to tell if the tweet posted received any r
etweets or not(True:Yes, False: No)
33) retweets: How many actual number of retweets the current retweet 
received at time when you are running this code
```

