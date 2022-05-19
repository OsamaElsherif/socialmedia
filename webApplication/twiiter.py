from bs4 import BeautifulSoup as BS
from selenium import webdriver
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.common.keys import Keys
from werkzeug.wrappers import response
from data import Twitter
from scripts import tweeting
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import time

#login data
# username = Twitter['username']
# password = Twitter['password']

# salt storing
salt = b'\xec\x86\xc6\xcao?3`.\xe8\x86\x0b\xcd?I\x8dV\x808c\x94\x03\x95~\xf3\xb7<iV\xd9\xe1\x01'

def intializtion():
    # responses = {}
    # driver = webdriver.Edge('webdriver/edge/msedgedriver.exe')
    options = EdgeOptions()
    options.use_chromium = True
    options.add_experimental_option("prefs", { 
        "profile.default_content_setting_values.notifications": 1 
    })
    # options.add_argument("headless")
    # options.add_argument("disable-gpu")
    # driver = webdriver.Edge('webdriver/edge/msedgedriver.exe')
    driver = Edge('webdriver/edge/msedgedriver.exe', options=options)
    driver.get('https://twitter.com/login')
    time.sleep(5)
    return driver

def login(driver, email, password):
    # selecting the fields by name
    f_username = driver.find_element_by_name('session[username_or_email]')
    print('found the username field')
    f_username.send_keys(email)
    time.sleep(1)
    f_password = driver.find_element_by_name('session[password]')
    print('find the password field')
    f_password.send_keys(password)
    time.sleep(1)
    f_password.send_keys(Keys.RETURN)
    time.sleep(15)
    page_source = driver.page_source
    soup = BS(page_source, 'html.parser')
    AccountMenu = soup.find('div', {'aria-label' : 'Account menu'})
    if AccountMenu:
        # print("SUC::200")
        # print(AccountMenu)
        # scrapping(soup)
        return 'SUC::200'
    else:
        return "ERR::300"

def scrapping(soup):
    print("Loggred in successfully")

    # Code goes here for parsing
    timeline = soup.find('div', {'aria-label' : 'Timeline: Your Home Timeline'})
    timeline_soup = BS(str(timeline), 'html.parser')
    # remeber : soup doesn't return str
    articles = timeline_soup.find_all('article')
    for article in articles:
        # article is actually the tweet
        # دي حنيكة ملناش دعوة بيها :"D
        article = str(article)
        article_soup = BS(article, 'html.parser')
        tweet = article_soup.find('div', {'data-testid' : 'tweet'})
        s = str(tweet)
        s_soup = BS(s, 'html.parser')
        scrapy = s_soup.find('div', {'class' : 'css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu'})
        s = str(scrapy)
        s_soup = BS(s, 'html.parser')
        scrapy = s_soup.find_all('div', {'class' : 'css-1dbjc4n'})

        # tweeted by user link
        user_info = str(scrapy[0])
        user_info_soup = BS(user_info, 'html.parser')
        l = user_info_soup.find('a', {'role' : 'link'})
        user_link = 'https://twitter.com'+l['href']

        # tweeted by name
        s_l = str(l)
        s_l_soup = BS(s_l, 'html.parser')
        twetted_by = s_l_soup.find('span').string

        # tests
        # tweet_info = str(scrapy[0])
        # print("0---0")
        # print(tweet_info)
        # print("0---0")

        # replays and likes, content
        tweet_info = str(scrapy[0])
        tweet_info_soup = BS(tweet_info, 'html.parser')
        try:
            replys_and_likes = tweet_info_soup.find('div', {'class' : 'css-1dbjc4n r-18u37iz r-1wtj0ep r-1s2bzr4 r-1mdbhws', 'role' : 'group'})['aria-label']
            replys_and_likes = str(replys_and_likes).split(',')
        except Exception as e:
            replys_and_likes = ''
            replys_and_likes = ''

        try:
            content = tweet_info_soup.find('div', {'class', 'css-901oao r-18jsvk2 r-1k78y06 r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0 r-1vmecro'}).string
        except Exception as e:
            try:
                content = tweet_info_soup.find('div', {'class', 'css-901oao r-18jsvk2 r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0'}).string
            except Exception as e:
                content = ''
                print(e)
                    
            
        # user img
        s = str(tweet)
        s_soup = BS(s, 'html.parser')
                
        scrapy = s_soup.find('div', {'class' : 'css-1dbjc4n r-1awozwy r-1hwvwag r-18kxxzh r-1b7u577'})
        user_img = s_soup.find('img')['src']

        try:
            scrappy_link = s_soup.find('div', { 'data-testid' :'card.wrapper'})
        except Exception as e:
            scrappy_link = ''

        try:
            scrappy_img = s_soup.find('div', {'class' : 'tweetPhoto', 'aria-label' : 'Image'})
        except Exception as e:
            scrappy_img = ""

        try:
            scrappy_retweet = article_soup.find('span', {'data-testid' : 'socialContext'})
        except Exception as e:
            scrappy_retweet = '' 
                
        try:
            scrappy_retweet = article_soup.find('span', string='Quote Tweet')
        except Exception as e:
            scrappy_retweet = ''
                

        # will be a list of data so it's okay in it to be a return.
        print('---------------------------- \n')
        print('Tweeted by : ')
        print(twetted_by)
        print('\n')
        print('User link : ')
        print(user_link)
        print('\n')
        print('User img : ')
        print(user_img)
        print('\n')
        print('replays and likes : ')
        print(replys_and_likes)
        print('\n')
        print('tweet content : ')
        print(content)
        print('\n')
        print(' link in tweet : ')
        print(scrappy_link)
        print('\n')
        print(' Image in tweet : ')
        print(scrappy_img)
        print('\n')
        print(' retweet : ')
        print(scrappy_retweet)

def tweet(driver, text):
    # print("Do you wan't to tweet !! ")
    # ans = input()
    # print("Write your tweet here : \n")
    # T = input() # the inputed text

    # encryption goes here
    # passw = "TesT123"
    # key = PBKDF2(passw, salt, dkLen=32)
    # data = bytes(text, 'utf-8')

    # cipher = AES.new(key, AES.MODE_CBC)
    # ciphered_data = cipher.encrypt(pad(data, AES.block_size))

    # iv storing
    # file_out = open("iv2.bin", "wb")
    # file_out.write(cipher.iv)
    # file_out.close()

    tweeting(text, driver)

##### OOP 

# class Twitter():
#     def __init__(self):
#         pass
    
#     def login(self):
#         pass

    
#     def scrapping(self):
#         pass
    
#     def wait(self):
#         pass

#     def tweeting(self, text):
#         # print("Do you wan't to tweet !! ")
#         # ans = input()
#         print("Write your tweet here : \n")
#         # T = input() # the inputed text
#         # encryption goes here
#         passw = "TesT123"
#         key = PBKDF2(passw, salt, dkLen=32)
#         data = bytes(text, 'utf-8')

#         cipher = AES.new(key, AES.MODE_CBC)
#         ciphered_data = cipher.encrypt(pad(data, AES.block_size))

#         # iv storing
#         file_out = open("iv2.bin", "wb")
#         file_out.write(cipher.iv)
#         file_out.close()

#         ret = tweeting(ciphered_data, self.driver)
#         if ret == "SUCC":
#             tweeting(self.driver)
#         else:
#             print("Okay :3")

# OOP => problem is the instienace
# functional programming =>