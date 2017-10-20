from urllib import request, parse, error
import json

host = 'http://aliv2.data.moji.com'
path = '/whapi/json/aliweather/briefforecast3days'
method = 'POST'
appcode = 'appCode'  # https://market.aliyun.com/products/57096001/cmapi013824.html?spm=5176.730005-57096001.0.0.upxMn8
querys = ''
bodys = {}
url = host + path


def getLocation():
    try:
        response = request.urlopen("http://freegeoip.net/json/")
        if response.status == 200:
            responseJson = json.loads(response.read())
            return responseJson.get("latitude"), responseJson.get("longitude")
    except:
        print('ERROR: Location not found!')
    return None, None


myLat, myLon = getLocation()
bodys['lat'] = myLat
bodys['lon'] = myLon
bodys['token'] = '443847fa1ffd4e69d929807d42c2db1b'
post_data = parse.urlencode(bodys).encode(encoding='utf8')
req = request.Request(url, data=post_data)
req.add_header('Authorization', 'APPCODE ' + appcode)
# 根据API的要求，定义相对应的Content-Type
req.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
try:
    response = request.urlopen(req)
    content = json.loads(response.read().decode())
    if content['code'] == 0:
        print('\t天气\t温度\t风向\t风力')
        for l in content['data']['forecast']:
            print('--------------------------------------------------------')
            print(l['predictDate'] + '\t' + l['updatetime'] + '(update)')
            print('白天:\t' + l['conditionDay'] + '  \t' + l['tempDay'] + '℃  \t'
                  + l['windDirDay'] + '  \t' + l['windLevelDay'])
            print('夜间:\t' + l['conditionNight'] + '  \t' + l['tempNight'] + '℃  \t'
                  + l['windDirNight'] + '  \t' + l['windLevelNight'])
except:
    print('ERROR: API request err!')
    pass
input('Please input any key for exit:')


