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
tablename = 'pages'
conn = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='mysql', charset='utf8')
cur = conn.cursor()
cur.execute('USE wyq')
try:
    cur.execute('CREATE TABLE '+tablename+' (id BIGINT(7) NOT NULL AUTO_INCREMENT, name VARCHAR(100), city VARCHAR(20), height VARCHAR(10), weight VARCHAR(10), homepage VARCHAR(100), profile VARCHAR(100), pic VARCHAR(100), created TIMESTAMP DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY(id))')
except pymysql.err.InternalError as e:
    print(e)

cur.execute('ALTER DATABASE wyq CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci')
cur.execute('ALTER TABLE '+tablename+' CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
cur.execute('ALTER TABLE '+tablename+' CHANGE name name VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
cur.execute('ALTER TABLE '+tablename+' CHANGE city city VARCHAR(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
cur.execute('ALTER TABLE '+tablename+' CHANGE height height VARCHAR(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
cur.execute('ALTER TABLE '+tablename+' CHANGE weight weight VARCHAR(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
cur.execute('ALTER TABLE '+tablename+' CHANGE homepage homepage VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
cur.execute('ALTER TABLE '+tablename+' CHANGE profile profile VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
cur.execute('ALTER TABLE '+tablename+' CHANGE pic pic VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')

def store(name, city, height, weight, hompage, profile, pic):
    cur.execute('INSERT INTO '+tablename+' (name, city, height, weight, homepage, profile, pic) VALUES (\"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\")', (name, city, height, weight, hompage, profile, pic))
    cur.connection.commit()


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
        temp['id'] = str(l['userId'])
        temp['name'] = l['realName']
        temp['city'] = l['city']
        temp['height'] = str(l['height'])
        temp['weight'] = str(l['weight'])
        temp['favornum'] = str(l['totalFavorNum'])
        temp['profile'] = 'http:'+l['avatarUrl']
        temp['pic'] = 'http:'+l['cardUrl']
        #print(temp)
        #mmList.append(temp)
        mkdir(temp['name'])
        print('%s正在抓取%s'%(page, temp['name']))
        getImg(temp['profile'], temp['name'], 'profile')
        getImg(temp['pic'], temp['name'], 'pic')
        if not os.path.exists('./'+temp['name']+'/info.txt'):
            with open('./'+temp['name']+'/info.txt', 'w') as f:
                f.write(temp['name']+'\n')
                f.write(temp['city']+'\n')
                f.write(temp['height']+'\n')
                f.write(temp['weight']+'\n')
        store(temp['name'], temp['city'], temp['height'], temp['weight'], 'https://mm.taobao.com/self/aiShow.htm?userId='+temp['id'], temp['profile'], temp['pic'])
    #return mmList


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


if __name__ == '__main__':
    page = 1
    while True:
        content = getJson(page)
        if content == -1:
            print('抓取完毕！')
            exit()
        parserJson(content, page)
        page += 1


