# 获取个人微博首页内容
from urllib import request, parse
import json, re

params = {'s': '******',
          'gsid': '******',
          'source': '******',
          'c': 'windows8',
          'wm': '9007_1139',
          'from': '******',
          'lang': 'zh_CN',
          'since_id': '',
          'max_id': '',
          'count': '20',
          'page': '',
          'feature': '0',
          'v_p': '13',
          'ua': '20156__weibo__2.2.1__win8__win8pad'
          }
url = 'https://api.weibo.cn/2/statuses/friends_timeline?'
headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows OS 8; Trident/3.1; IEMobile/7.0; Microsoft; Windows8_SINA)',
           'Host': 'api.weibo.cn'
           }

def getCode(max_id=''):
    params['max_id'] = max_id
    full_url = url + parse.urlencode(params)
    req = request.Request(full_url, headers=headers)
    try:
        code = request.urlopen(req)
    except:
        print('Request Error!')
        return
    if code.code == 200:
        # print(json.loads(code.read()))
        return json.loads(code.read())


def jsonParse(js_code):
    next_cursor = js_code['next_cursor']
    print(next_cursor)
    content = js_code['statuses']
    for c in content:
        print(c['user']['name'], '  ', c['reposts_count'], c['comments_count'], c['attitudes_count'])
        try:
            source = re.findall(re.compile(r'>(.*?)<'), c['source'])[0]
        except:
            source = ''
            print('Source Error!')
        print(c['created_at'], source)
        print(c['text'])
        print('-------------------------------------------------')
    return next_cursor


text_id = set()
text_id.add('')
count = 0
next_cursor = jsonParse(getCode())
while True:
    if next_cursor not in text_id:
        text_id.add(next_cursor)
        next_cursor = jsonParse(getCode(next_cursor))
    else:
        count += 1
    if count >= 2:
        print('Over!')
        break

