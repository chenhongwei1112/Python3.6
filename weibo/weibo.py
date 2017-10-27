from urllib import request, parse
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from collections import OrderedDict
import json
import html

cookie = 'your cookie'
host = 'weibo.com'
referer = ''
user_agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Mobile Safari/537.36'
headers = {#'Cookie':cookie,
           'Host':host,
           #'Referer':referer,
           'User-Agent':user_agent
           }

def getText(uid, para=None):
    desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
    desired_capabilities['phantomjs.page.settings.userAgent'] = headers
    desired_capabilities['phantomjs.page.settings.loadImages'] = False
    driver = webdriver.PhantomJS(executable_path='/home/wyq/application/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
    driver.start_session(desired_capabilities)
    for coo in re.split(';', cookie.replace(' ', '')):
        cookieDict = {'name':coo.split('=')[0],
                      'value':coo.split('=')[1],
                      'domain':'.weibo.com',
                      'path':'/'
                      }
        driver.add_cookie(cookieDict)
    #print(driver.get_cookies())
    if para is None:
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
    else:
        url = para
    #print(url)
    driver.get(url)
    #time.sleep(10)
    #print(driver.page_source)
    text = driver.page_source
    driver.close()
    return text

def getHtmlFromText(text):
    r = re.compile('(<div .*/div>)')
    code = r.findall(text)[0]
    clearText = code.replace(r'\"', '"').replace(r'\/', '/').replace(r'\n', '')
    #print(clearText)
    clearText = re.sub(r'( {2,})', ' ', clearText)
    #print(clearText)
    return clearText

def html_parser(html, flag):
    soup = BeautifulSoup(html, 'lxml')
    if flag == 1:
        div = soup.findAll('div', {'class':'WB_feed', 'module-type':'feed'})
        content = div[0].findAll('div', {'class':'WB_detail'})
    elif flag == 0:
        content = soup.findAll('div', {'class':'WB_detail'})
    #f = open('3.txt', 'w')
    for c in content:
        post_people = c.find('div', {'class':'WB_info'}).find('a').get_text()
        subTitleL = c.findAll('div', {'class':'WB_from S_txt2'})[0].findAll('a')
        post_subtitle = ''
        for l in subTitleL:
            post_subtitle += l.get_text()
        post_content = c.find('div', {'class':'WB_text W_f14'}).get_text()
        #f.write('%s %s %s'%(post_people,post_subtitle,post_content))
        print(post_people, ' ', post_subtitle,' ',post_content)
    #f.close()

def getNextText(uid=None, para=None):
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
         ('pagebar', para),
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
    driver.get(url)
    text = driver.page_source
    driver.close()
    return text

def getNextHtmlFromText(text):
    r = re.compile('(\{.*\})')
    code = r.findall(text)[0]
    content = json.loads(code)['data']
    content = content.replace(r'\n', '')
    content = re.sub(r'( {2,})', ' ', content)
    #html_ = html.unescape(content)
    html_ = content.replace('&quto;', '"').replace('&amp;', '&').replace('&lt;', '<')
    html_ = html_.replace('&gt;', '>').replace('&nbsp;', ' ')

    return html_

def findNextPage(html):
    soup = BeautifulSoup(html, 'lxml')
    #print(soup)
    div = soup.findAll('div', {'node-type':'feed_list_page'})[0].findAll('li')
    pageList = []
    for l in div:
        pageList.append('https://weibo.com'+l.find('a')['href'])
    return pageList

text = getText(1928010053)
html_ = getHtmlFromText(text)
html_parser(html_, 1)
text = getNextText(1928010053, 0)
html_ = getNextHtmlFromText(text)
html_parser(html_,0)
text = getNextText(1928010053, 1)
html_ = getNextHtmlFromText(text)
html_parser(html_,0)
pageList = findNextPage(html_)
'''
for l in pageList:
    text = getText(uid=None,para=l)
    print(text)
    
    html_ = getHtmlFromText(text)
    html_parser(html_, 0)
'''
