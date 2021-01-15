# twitter_web_crawler

<h1> Twitter web crawler </h1>

Script created to collect data from Twitter website. 

Available methods:
- search by userid
- search by hashtags
- search by link


Example of usage:

```python
import os
current_path = os.path.dirname(os.path.abspath(__file__))
full_path = os.path.join(current_path,'geckodriver.exe')
tweet_tester = TwitterScrappy(full_path)
tweets = tweet_tester.search_by_user('warcraft', n_scrolls=20)
```


Dependencies:
- Selenium 
- Geckodriver (for Selenium webdriver)
