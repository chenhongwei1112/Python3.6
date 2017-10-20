from urllib import request, parse
import json

host = 'http://jisuznwd.market.alicloudapi.com'
path = '/iqa/query'
method = 'GET'
appcode = 'appCode'
bodys = {}

while True:
    question = dict()
    question['key'] = input()
    querys = 'question='+parse.urlencode(question).replace('key=','')

    url = host + path + '?' + querys

    req = request.Request(url)
    req.add_header('Authorization', 'APPCODE ' + appcode)
    try:
        response = request.urlopen(req)
        content = json.loads(response.read().decode('utf-8'))
        #print(content)
        if content['msg'] == 'ok':
            print(content['result']['content'])
    except:
        print('Error!')

