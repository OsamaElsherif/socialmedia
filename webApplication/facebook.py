from bs4 import BeautifulSoup as BS
from bs4.element import AttributeValueWithCharsetSubstitution
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from msedge.selenium_tools import EdgeOptions, Edge
from scripts import posting
import time
from data import Facebook

#login data
# email = Facebook['email']
# password = Facebook['password']

def intializtion():
    # responses = {}
    options = EdgeOptions()
    options.use_chromium = True
    options.add_experimental_option("prefs", { 
        "profile.default_content_setting_values.notifications": 1 
    })
    # options.add_argument("headless")
    # options.add_argument("disable-gpu")
    # driver = webdriver.Edge('webdriver/edge/msedgedriver.exe')
    driver = Edge('webdriver/edge/msedgedriver.exe', options=options)
    driver.get('https://facebook.com')
    time.sleep(5)
    # login(driver, 'elsherifosama225@gmail.com', 'osama3502')
    return driver

def login(driver, email, password):
    # selecting the fields by the name
    f_username = driver.find_element_by_name('email')
    f_username.send_keys(email)
    time.sleep(1)
    f_password = driver.find_element_by_name('pass')
    f_password.send_keys(password)
    time.sleep(1)
    f_password.send_keys(Keys.RETURN)
    time.sleep(15)
    page_source = driver.page_source
    soup = BS(page_source, 'html.parser')
    AccountMenu = soup.find('div', {'aria-label' : 'Account Controls and Settings'})
    if AccountMenu:
        # print("SUC::200")
        # print(AccountMenu)
        # scrapping(soup)
        # post(driver, 'Test')
        return 'SUC::200'
    else:
        return "ERR::300"

def scrapping(source, level, driver):
    print("Logged In")
    soup = BS(source, 'html.parser')
    if level == 'profile':
        menu = str(soup.find('div', {'class' : 'l9j0dhe7 tr9rh885 buofh1pr cbu4d94t j83agx80', 'data-pagelet' : 'LeftRail'}))
        menu_soup = BS(menu, 'html.parser')
        anchors = menu_soup.find_all('a', {'role' : 'link'})
        profile_anchor = anchors[0]
        profile_link = profile_anchor['href']
        driver.get(profile_link)
        driver.execute_script('''window.scrollBy(0, 1000);''')
        time.sleep(2)
        driver.execute_script('''window.scrollBy(0, 1000);''')
        time.sleep(2)
        driver.execute_script('''window.scrollBy(0, 1000);''')
        time.sleep(2)
        driver.execute_script('''window.scrollBy(0, 1000);''')
        time.sleep(2)
        driver.execute_script('''window.scrollBy(0, 1000);''')
        time.sleep(2)
        driver.execute_script('''window.scrollBy(0, 1000);''')
        time.sleep(2)
        driver.execute_script('''window.scrollBy(0, 1000);''')
        time.sleep(2)
        page_source = driver.page_source
        soup = BS(page_source, 'html.parser')
        timeline = soup.find('div', {'data-pagelet' : 'ProfileTimeline'})
        timeline_soup = BS(str(timeline), 'html.parser')
        posts = timeline_soup.find_all('div')
        result = []
        # result.clear()
        for post in posts:
            post_soup = BS(str(post), 'html.parser')
            content = post_soup.find('div', {'data-ad-comet-preview' : 'message', 'data-ad-preview' : 'message'})
            content_soup = BS(str(content), 'html.parser')
            try:
                text = content_soup.find('span').text
                if result.count(text) > 0:
                    pass
                else:
                    result.append(text)
            except:
                pass
        return result
    else:
        # code goes here for parsing
        feed = soup.find('div', {'role' : 'feed'})
        feed_soup = BS(str(feed), 'html.parser')
        articles = feed_soup.find_all('div', {'role' : 'article'})

        for article in articles:
            post = str(article)
            post_soup = BS(post, 'html.parser')

            a = post_soup.find('a', {'class' : 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl oo9gr5id gpro0wi8oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl oo9gr5id gpro0wi8'})
            a_soup = BS(str(a), 'html.parser')

            # user link
            try:
                link = a
                # ['href']
            except Exception as e:
                link = e

            # user image
            try:
                image = a_soup.find('image')
                # ['xlink:href']
            except Exception as e:
                image = e

            div = post_soup.find('div', {'class' : 'j83agx80 cbu4d94t ew0dbk1b irj2b8pg'})
            span = BS(str(div), 'html.parser')
            
            # user name not username
            try:
                username = span.find('span', {'class' : 'd2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d3f4x2em fe6kdd0r mau55g9w c8b282yb iv3no6db jq4qci2q a3bd9o3v knj5qynh m9osqain hzawbc8m'})
            except Exception as e:
                username = e

            # post content
            try:
                post_contnet = post_soup.find('div', {'data-ad-comet-preview' : 'message', 'data-ad-preview' : 'message'})
            except Exception as e:
                post_contnet = e


            # print('User Link : ')
            # print(link)
            # print('User Image : ')
            # print(image)
            result = {
                'username' : username,
                'content' : post_contnet
            }
            return result
            # if username:
            #     print("---------------")
            #     print('User Name : ')
            #     print(username)
            #     print('Post Content : ')
            #     print(post_contnet)

def post(driver, post):
    posting(post, driver)
