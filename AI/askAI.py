from urllib import request, parse
import json
import datetime

host = 'http://jisuznwd.market.alicloudapi.com'
path = '/iqa/query'
method = 'GET'
appcode = 'appCode' #https://market.aliyun.com/products/57124001/cmapi013943.html?spm=5176.2020520132.101.5.bdy3yT
bodys = {}

while True:
    question = dict()
    print(datetime.datetime.now())
    question['key'] = input('我：')
    print()
    querys = 'question='+parse.urlencode(question).replace('key=','')

    url = host + path + '?' + querys

    req = request.Request(url)
    req.add_header('Authorization', 'APPCODE ' + appcode)
    try:
        response = request.urlopen(req)
        content = json.loads(response.read().decode('utf-8'))
        #print(content)
        if content['msg'] == 'ok':
            print(datetime.datetime.now())
            print('AI：'+content['result']['content'])
            print()
    except:
        print('Error!')

