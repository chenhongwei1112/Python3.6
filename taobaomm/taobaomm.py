from urllib import request, parse, error
import json
import os
import pymysql

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
param = {'_input_charset': 'utf-8',
          'q': '',
          'viewFlag': 'A',
          'sortType': 'default',
          'searchStyle': '',
          'searchRegion': 'city',
          'searchFansNum': '',
          'currentPage': '',
          'pageSize': '20'
          }
url = 'https://mm.taobao.com/tstar/search/tstar_model.do'


def getJson(page):
    param['currentPage'] = str(page)
    params = parse.urlencode(param).encode('utf-8')
    req = request.Request(url, data=params, headers=headers)
    content = request.urlopen(req)
    content = json.loads(content.read().decode('gbk'))
    if content['status'] == -1:
        return -1
    #print(content)
    return content

def parserJson(content, page):
    mmList = []

    data = content['data']['searchDOList']
    for l in data:
        temp = {}
        temp['id'] = l['userId']
        temp['name'] = l['realName']
        temp['city'] = l['city']
        temp['height'] = l['height']
        temp['weight'] = l['weight']
        temp['favornum'] = l['totalFavorNum']
        temp['profile'] = 'http:'+l['avatarUrl']
        temp['pic'] = 'http:'+l['cardUrl']
        #print(temp)
        mmList.append(temp)
        mkdir(temp['name'])
        print('%s正在抓取%s'%(page, temp['name']))
        getImg(temp['profile'], temp['name'], 'profile')
        getImg(temp['pic'], temp['name'], 'pic')
        with open('./'+temp['name']+'/info.txt', 'w') as f:
            f.write(temp['name']+'\n')
            f.write(temp['city']+'\n')
            f.write(temp['height']+'\n')
            f.write(temp['weight']+'\n')

    return mmList


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        print('目录已存在！')


def getImg(url, path, name):
    if os.path.exists('./' + path + '/' + name + '.jpg'):
        print('文件已存在！')
        return 0
    try:
        req = request.Request(url, headers=headers)
        reponse = request.urlopen(req)
        get_img = reponse.read()
        with open('./' + path + '/' + name + '.jpg', 'wb') as fp:
            fp.write(get_img)
    except error.URLError as e:
        print(e.reason)

if __name__=='__main__':
    page = 1
    while True:
        content = getJson(page)
        if content == -1:
            print('抓取完毕！')
            exit()
        mm = parserJson(content, page)
        page += 1


