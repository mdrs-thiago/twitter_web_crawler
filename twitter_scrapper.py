from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import os, re
from time import sleep


class TwitterScrappy:
    def __init__(self, path):
        self.path = path
        init_browser()

    def init_browser(self):
        options = Options()
        options.headless = True
        self.browser = webdriver.Firefox(executable_path = self.path, options=options)
        self.browser.implicitly_wait(15)

    def search_by_user(self,userid, n_scrolls=10):
        '''
        Collet data from Twitter user using only it's ID. 

        INPUT:
        - userid: @ of user of interest
        - n_scrolls: Number of scrolls to get more data.

        OUTPUT: 
        - tweets: List of tweet dictionary. Can be converted to JSON file.
        '''
        try:
            self.browser.get('https://twitter.com/{}'.format(userid))
            tweets = self.query_tweets(n_scrolls)
            return tweets

        except Exception as e:
            print(e)
            return None

    def search_by_hashtag(self, hashtag, n_scrolls=10):
        '''
        Collet data from Twitter info from hashtags. 

        INPUT:
        - hashtags - topic of interest.
        - n_scrolls: Number of scrolls to get more data.

        OUTPUT: 
        - tweets: List of tweet dictionary. Can be converted to JSON file.
        '''

        try:
            self.browser.get('https://twitter.com/search?q={}&src=trend_click&vertical=trends'.format(hashtag))
            tweets = self.query_tweets(n_scrolls)
            return tweets

        except Exception as e:
            print(e)
            return None

    def search_by_link(self, link, n_scrolls = 10):
        '''
        Collet data from Twitter directly from link. 

        INPUT:
        - userid: @ of user of interest
        - n_scrolls: Number of scrolls to get more data.

        OUTPUT: 
        - tweets: List of tweet dictionary. Can be converted to JSON file.
        '''
        p = re.compile("^(https?://)?(www.)?twitter.com/[a-z]")
        if p.match(link) is None:
            print('Link not valid.')
            return None 

        try:
            self.browser.get(link)
            tweets = self.query_tweets(n_scrolls)
            return tweets

        except Exception as e:
            print(e)
            return None


    def query_tweets(self, n_scrolls):
        '''
        Method for query tweets of TwitterScrappy. It uses key tag to extract the tweet container and then organize as follow:
        - Username: Name of twitter user
        - Userid: @ of user
        - Date: Datetime of tweet
        - Tweet: Text itself
        - Likes: Likes of that tweet
        - Retweets: Retweets of that tweet
        - Comments: Comments of that tweet

        INPUT: 
        - n_scrolls: Number of times that TwitterScrappy will roll down and get data

        OUTPUT:
        - tweet_dict: List of tweet dictionaries.
        '''
        #All tweets are labeled as a div with data-testid attribute.
        tweet_content = ('//div[@data-testid="tweet"]')

        #List of tweets info
        tweet_dict = []

        #Twitter uses a dynamic DOM, so to get the tweets, we scroll down and get all available tweets.
        #TODO This procedure can be problematic, because some tweets can be skipped or duplicated
        for n in range(n_scrolls):
            #Scroll down every iteration
            self.browser.find_element_by_xpath('//body').send_keys(Keys.END)
            #Sleep time for 3 sec. to prevent overload problems (Twitter recommends 1 sec at least)
            sleep(3)


            for tweet_container in self.browser.find_elements_by_xpath(tweet_content):
                try:
                    raw_tweet = tweet_container.text.split('\n')
                    username = raw_tweet[0]
                    userid = raw_tweet[1]
                    date = tweet_container.find_element_by_tag_name('time').get_attribute('datetime')
                    tweet = tweet_container.find_element_by_xpath('./div[2]/div[2]/div[1]/div').text
                    
                    comments = tweet_container.find_element_by_xpath('.//div[@role="group"]/div[1]').text
                    retweets = tweet_container.find_element_by_xpath('.//div[@role="group"]/div[2]').text
                    likes = tweet_container.find_element_by_xpath('.//div[@role="group"]/div[3]').text
                except Exception as e:
                    print(e)
                    pass
                t_dict = {'username': username, 'userid': userid, 'date': date, 'tweet': tweet, 'likes': likes, 'retweets': retweets, 'comments': comments}
                tweet_dict.append(t_dict)
        return tweet_dict

#%% 
from selenium import webdriver
import os
from time import sleep
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

class TwitterData:
    def __init__(self,user_id):
        self.user_id = user_id 


    @staticmethod
    def wait_loading(self, time):
        for i in range(time):
            sleep(1)

#print(os.path.dirname(os.path.abspath(__file__)))
current_path = os.path.dirname(os.path.abspath(__file__))
full_path = os.path.join(current_path,'geckodriver.exe')
options = Options()
options.headless = True

#post_element_xpath = '/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[2]/section/div/div'
a = './/*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[2]/section/div/div'

browser = webdriver.Firefox(executable_path = full_path, options=options)
browser.implicitly_wait(15)
#browser.get('https://twitter.com/warcraft')
browser.get()

n_scrolls = 3



#For users
#tweet_content = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/div[2]/section/div/div/div'
                 #//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[2]/section/div/div
#For hashtags
#tweet_content = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div/div'
tweet_content = ('//div[@data-testid="tweet"]')
tweets = []
tweet_dict = []
r_idx = 0
for k in range(n_scrolls):
    browser.find_element_by_xpath('//body').send_keys(Keys.END)
    sleep(5)
    for idx, tweet_container in enumerate(browser.find_elements_by_xpath(tweet_content)):
        print(idx + r_idx)

        try:
#.//article/div/div/div/div[2]/div[2]/div[1]/div/div/div[1]/div[1]/a/div/div[1]            
            raw_tweet = tweet_container.text.split('\n')
            username = raw_tweet[0]
            userid = raw_tweet[1]
            date = tweet_container.find_element_by_tag_name('time').get_attribute('datetime')
            #tweet = i.find_element_by_xpath('.//article/div/div/div/div[2]/div[2]/div[2]/div[1]/div').text
            tweet = tweet_container.find_element_by_xpath('./div[2]/div[2]/div[1]/div').text
            
            comments = tweet_container.find_element_by_xpath('.//div[@role="group"]/div[1]').text
            retweets = tweet_container.find_element_by_xpath('.//div[@role="group"]/div[2]').text
            likes = tweet_container.find_element_by_xpath('.//div[@role="group"]/div[3]').text
            print('USER {} USERID {}, \n {} with {} comments, {} retweets and {} likes'.format(username, userid, tweet, comments, retweets, likes))
        except Exception as e:
            print(e)
            pass
            '''
            raw_tweet = i.text 
            splited_tweet = raw_tweet.split('\n')
            #print(raw_tweet)
            if len(splited_tweet) < 5:
                continue
            username = splited_tweet[0]
            userid = splited_tweet[1]

            #Check if userid starts with pattern @
            if not userid.startswith('@'):
                continue 
            else:
                splited_tweet.pop(0) #Pop usarname from splited tweet
                splited_tweet.pop(1) #Pop userid from splited tweet
            
            date = splited_tweet[1] 
            tweet = splited_tweet[2]

            likes = splited_tweet[-1]
            #retweets = splited_tweet[-2]
            comments = splited_tweet[-3]
            #Check if first Tweet is Fixed or not 
            '''
        t_dict = {'username': username, 'userid': userid, 'date': date, 'tweet': tweet, 'likes': likes, 'retweets': retweets, 'comments': comments}
        tweet_dict.append(t_dict)



# %%
len(tweet_dict)
# %%
tweet_dict
tweet_dict[30]
# %%
len(tweet_dict)
# %%
tweet_dict[36]['likes']
# %%
tweet_dict
# %%
import re 
# %%
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

import os, re
from time import sleep


class TwitterScrappy:
    def __init__(self, path):
        self.path = path
        self.init_browser()

    def init_browser(self):
        options = Options()
        options.headless = True
        self.browser = webdriver.Firefox(executable_path = self.path, options=options)
        self.browser.implicitly_wait(15)

    def search_by_user(self,userid, n_scrolls=10):
        '''
        Collet data from Twitter user using only it's ID. 

        INPUT:
        - userid: @ of user of interest
        - n_scrolls: Number of scrolls to get more data.

        OUTPUT: 
        - tweets: List of tweet dictionary. Can be converted to JSON file.
        '''
        try:
            self.browser.get('https://twitter.com/{}'.format(userid))
            tweets = self.query_tweets(n_scrolls)
            return tweets

        except Exception as e:
            print(e)
            return None

    def search_by_hashtag(self, hashtag, n_scrolls=10):
        '''
        Collet data from Twitter info from hashtags. 

        INPUT:
        - hashtags - topic of interest.
        - n_scrolls: Number of scrolls to get more data.

        OUTPUT: 
        - tweets: List of tweet dictionary. Can be converted to JSON file.
        '''

        try:
            self.browser.get('https://twitter.com/search?q={}&src=trend_click&vertical=trends'.format(hashtag))
            tweets = self.query_tweets(n_scrolls)
            return tweets

        except Exception as e:
            print(e)
            return None

    def search_by_link(self, link, n_scrolls = 10):
        '''
        Collet data from Twitter directly from link. 

        INPUT:
        - userid: @ of user of interest
        - n_scrolls: Number of scrolls to get more data.

        OUTPUT: 
        - tweets: List of tweet dictionary. Can be converted to JSON file.
        '''
        p = re.compile("^(https?://)?(www.)?twitter.com/[a-z]")
        if p.match(link) is None:
            print('Link not valid.')
            return None 

        try:
            self.browser.get(link)
            tweets = self.query_tweets(n_scrolls)
            return tweets

        except Exception as e:
            print(e)
            return None


    def query_tweets(self, n_scrolls):
        '''
        Method for query tweets of TwitterScrappy. It uses key tag to extract the tweet container and then organize as follow:
        - Username: Name of twitter user
        - Userid: @ of user
        - Date: Datetime of tweet
        - Tweet: Text itself
        - Likes: Likes of that tweet
        - Retweets: Retweets of that tweet
        - Comments: Comments of that tweet

        INPUT: 
        - n_scrolls: Number of times that TwitterScrappy will roll down and get data

        OUTPUT:
        - tweet_dict: List of tweet dictionaries.
        '''
        #All tweets are labeled as a div with data-testid attribute.
        tweet_content = ('//div[@data-testid="tweet"]')

        #List of tweets info
        tweet_dict = []

        #Twitter uses a dynamic DOM, so to get the tweets, we scroll down and get all available tweets.
        #TODO This procedure can be problematic, because some tweets can be skipped or duplicated
        for n in range(n_scrolls):
            #Scroll down every iteration
            self.browser.find_element_by_xpath('//body').send_keys(Keys.END)
            #Sleep time for 3 sec. to prevent overload problems (Twitter recommends 1 sec at least)
            sleep(3)


            for tweet_container in self.browser.find_elements_by_xpath(tweet_content):
                try:
                    raw_tweet = tweet_container.text.split('\n')
                    username = raw_tweet[0]
                    userid = raw_tweet[1]
                    date = tweet_container.find_element_by_tag_name('time').get_attribute('datetime')
                    tweet = tweet_container.find_element_by_xpath('.//div[2]/div[2]/div[1]/div').text
                    
                    comments = tweet_container.find_element_by_xpath('.//div[@role="group"]/div[1]').text
                    retweets = tweet_container.find_element_by_xpath('.//div[@role="group"]/div[2]').text
                    likes = tweet_container.find_element_by_xpath('.//div[@role="group"]/div[3]').text
                except Exception as e:
                    print(e)
                    pass
                t_dict = {'username': username, 'userid': userid, 'date': date, 'tweet': tweet, 'likes': likes, 'retweets': retweets, 'comments': comments}
                tweet_dict.append(t_dict)
        return tweet_dict


# %%
current_path = os.path.dirname(os.path.abspath(__file__))
full_path = os.path.join(current_path,'geckodriver.exe')
tweet_tester = TwitterScrappy(full_path)
# %%
tweets = tweet_tester.search_by_user('luide', n_scrolls=20)
# %%
len(tweets)
# %%
tweets
# %%
