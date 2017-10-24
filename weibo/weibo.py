from urllib import request, parse
from bs4 import BeautifulSoup
import re
from selenium import webdriver
import time
from collections import OrderedDict
#import sys

cookie = ''
host = ''
referer = ''
user_agent = ''
headers = {'Cookie':cookie,
           'Host':host,
           'Referer':referer,
           'User-Agent':user_agent
           }

def getText(uid):
    driver = webdriver.PhantomJS(executable_path='/home/wyq/application/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
    for coo in re.split(';', cookie.replace(' ', '')):
        cookieDict = {'name':coo.split('=')[0],
                      'value':coo.split('=')[1],
                      'domain':'.weibo.com',
                      'path':'/'
                      }
        driver.add_cookie(cookieDict)
    #print(driver.get_cookies())
    params = OrderedDict(
        [('pids','Pl_Official_MyProfileFeed__22'),
         ('profile_ftype','1'),
         ('is_all','1'),
         ('ajaxpagelet','1'),
         ('ajaxpagelet_v6','1')
         ])
    params['__ref'] = '/u'+str(uid)+'?profile_ftype='+params['profile_ftype']+'&is_all='+params['is_all']+'#_0'
    params['_t'] = 'FM_'+str(int(time.time()*100000))
    url = 'https://weibo.com/u/'+str(uid)+'?'+parse.urlencode(params)
    #print(url)
    driver.get(url)
    #time.sleep(10)
    #print(driver.page_source)
    return driver.page_source

def getHtmlFromText(text):
    r = re.compile('(<div .*/div>)')
    code = r.findall(text)[0]
    clearText = code.replace(r'\"', '"').replace(r'\/', '/').replace(r'\n', '')
    #print(clearText)
    clearText = re.sub(r'( {2,})', ' ', clearText)
    #print(clearText)
    return clearText

def html_parser(html):
    soup = BeautifulSoup(html, 'lxml')
    div = soup.findAll('div', {'class':'WB_feed', 'module-type':'feed'})
    content = div[0].findAll('div', {'class':'WB_detail'})
    for c in content:
        post_people = c.find('div', {'class':'WB_info'}).find('a').get_text()
        post_subtitle = c.findAll('div', {'class':'WB_from S_txt2'})[0].get_text()
        post_content = c.find('div', {'class':'WB_text W_f14'}).get_text()
        print(post_people, '\t\t', post_subtitle,'\t\t',post_content)

def getNextText(uid):
    driver = webdriver.PhantomJS(executable_path='/home/wyq/application/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
    for coo in re.split(';', cookie.replace(' ', '')):
        cookieDict = {'name':coo.split('=')[0],
                      'value':coo.split('=')[1],
                      'domain':'.weibo.com',
                      'path':'/'
                      }
        driver.add_cookie(cookieDict)
    params = OrderedDict(
        [('ajwvr', '6'),
         ('domain','100505'),
         ('profile_ftype', '1'),
         ('is_all', '1'),
         ('pagebar', '1'),
         ('pl_name','Pl_Official_MyProfileFeed__22'),
         ('id','100505'+str(uid)),
         ('script_uri','/u/'+str(uid)),
         ('feed_type','0'),
         ('page','1'),
         ('pre_page','1'),
         ('domain_op', '100505')
         ])
    params['__rnd'] = str(int(time.time()*100000))
    url = 'https://weibo.com/p/aj/v6/mblog/mbloglist?'+parse.urlencode(params)
    #print(url)
    driver.get(url)
    print(driver.page_source.encode('gbk'))

text = getText(1928010053)
html = getHtmlFromText(text)
html = html_parser(html)
getNextText(1928010053)
