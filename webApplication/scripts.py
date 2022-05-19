# this file is for all the external scripts will be used in the lib
# ctrl + enter => tweeting (The key compination)

from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def tweeting(tweet, driver):
    if len(tweet) > 250:
        return "ERR: Can't tweet more than 250 characters"
    else:
        # code goes here
        driver.get('https://twitter.com/compose/tweet')

        time.sleep(15)
        page_source = driver.page_source
        soup = BS(page_source, 'html.parser')

        # selecting the texrarea D":
        # textarea = soup.find('div', {'data-testid' : 'tweetTextarea_0'})
        textarea = driver.find_element_by_xpath("//div[@data-testid='tweetTextarea_0']")
        textarea.send_keys(str(tweet))
        textarea.send_keys(Keys.CONTROL + Keys.RETURN)
        # button = soup.find('div', {'data-testid' : 'tweetButton'})

        print("Tweeted Successfully")

def posting(post, driver):
    # page_source = driver.page_source
    field = driver.find_element_by_xpath("//div[@class='oajrlxb2 b3i9ofy5 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 j83agx80 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x cxgpxx05 d1544ag0 sj5x9vvc tw6a2znq i1ao9s8h esuyzwwr f1sip0of lzcic4wl l9j0dhe7 abiwlrkh p8dawk7l bp9cbjyn orhb3f3m czkt41v7 fmqxjp7s emzo65vh btwxx1t3 buofh1pr idiwt2bm jifvfom9 kbf60n1y']")
    field.click()
    # textbox = driver.find_element_by_xpath("//div[@role='textbox']")
    time.sleep(5)
    textbox = driver.find_element_by_xpath("//div[@style='outline: none; user-select: text; white-space: pre-wrap; overflow-wrap: break-word;']")
    textbox.click()
    textbox.send_keys(str(post))
    textbox.send_keys(Keys.CONTROL + Keys.RETURN)

