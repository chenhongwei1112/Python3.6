# _*_coding:utf-8_*_
from urllib import request, parse
import json

city = ''
postData1 = {'q': city,
            'mkt': 'zh-CN',
            'cjmapasschema': 'global',
            'ul': '39.907,116.388,100',
            'appid': 'C98EA5B0842DBB9405BBF071E1DA76512D21FE361',
            'mr': '5',
            'Client-AppVersion': '4.21.2212.0'
            }

postData2 = {# 'uints': 'C',
             # 'region': 'CN',
             'appId': '3CDAA343-A116-43BF-93EF-7B13D232AE7C1',
             'formcode': 'WTHRST',
             'Client-AppVersion': '4.21.2212.0'
             }

headers = {  # 'Accept-encoding': 'gzip',
           # 'X-Search-UILang': 'zh-CN',
           'User-Agent': 'X-Client/AppexWin8Microsoft.BingWeather X-Client-AppVersion/4.21.2212.0',
           'Host': 'platform.bing.com',
           'Connection': 'keep-Alive'
           }


def getCityInfo(q):
    postData1['q'] = q
    headers['X-Search-UILang'] = 'zh-CN'
    url = 'http://platform.bing.com/geo/AutoSuggest/v1?' + parse.urlencode(postData1)
    req = request.Request(url, headers=headers)
    # print(req.get_full_url())
    try:
        html = request.urlopen(req)
    except:
        print('城市信息查询失败！')
        return None
    # print(html.read())
    textjs = json.loads(html.read())

    headers.pop('X-Search-UILang')
    headers['Host'] = 'cn.service.weather.msn.com'
    postData2['locality'] = textjs['@graph'][0]['s:address']['s:name']
    try:
        postData2['adminDistrict'] = textjs['@graph'][0]['s:address']['s:addressRegion']
    except:
        postData2['adminDistrict'] = ''             # 直辖市
    postData2['countryRegion'] = ''
    postData2['isoCode'] = ''
    postData2['latitude'] = textjs['@graph'][0]['s:geo']['s:latitude']
    postData2['longitude'] = textjs['@graph'][0]['s:geo']['s:longitude']
    url = 'http://cn.service.weather.msn.com/zh-CN/locations/search/?'+parse.urlencode(postData2)
    # print(url)
    req = request.Request(url, headers=headers)
    try:
        html = request.urlopen(req)
    except:
        print('城市信息查询失败！')
        return None
    textjs = json.loads(html.read())
    # print(textjs['responses'][0]['locations'][0]['coordinates'])
    address = {'nameid': textjs['responses'][0]['locations'][0]['nameid'],
               'lat': textjs['responses'][0]['locations'][0]['coordinates']['lat'],
               'lon': textjs['responses'][0]['locations'][0]['coordinates']['lon']
               }
    # print(address)
    return address


def getWeather(geo, info):
    postData2['uints'] = 'C'
    postData2['region'] = 'CN'
    if info == 'summary':
        url = 'http://cn.service.weather.msn.com/zh-CN/weather/summary/'
    elif info == 'forecast_daily':
        url = 'http://cn.service.weather.msn.com/zh-CN/weather/forecast/daily/'
        postData2['nl'] = 'true'
    elif info == 'average':
        url = 'http://cn.service.weather.msn.com/zh-CN/weather/average/daily/'
        postData2['provider'] = 'WxTrend'
    elif info == 'forecast_trend':
        url = 'http://cn.service.weather.msn.com/zh-CN/weather/forecast/trend/'
        postData2['days'] = '10'
    else:
        return None
    headers['Host'] = 'cn.service.weather.msn.com'
    full_url = url+str(geo['lat'])+','+str(geo['lon'])+'?'+parse.urlencode(postData2)
    # print(full_url)

    req = request.Request(full_url, headers=headers)
    try:
        html = request.urlopen(req)
    except:
        print('天气信息获取失败！')
        return None
    textjs = json.loads(html.read())
    weather = textjs['responses'][0]

    if info == 'summary':
        getSummary(weather['weather'][0])
    elif info == 'forecast_daily':
        getForecastDaily(weather['weather'][0])
    elif info == 'average':
        getAverage(weather['average'][0])
    elif info == 'forecast_trend':
        getForecastTrend(weather)



def getSummary(weatherjs):
    print('--------------------------------------------------')
    print('更新时间：', weatherjs['current']['created'])
    print('预警信息: ', weatherjs['alerts'])
    print('当前温度：%s℃' % weatherjs['current']['temp'])
    print('当前天气：', weatherjs['current']['cap'])
    print('当前空气质量：%s(%s) '% (weatherjs['current']['aqiSeverity'], weatherjs['current']['aqi']))
    print('当前风向：%s\t风力：%s'%(weatherjs['current']['pvdrWindDir'], weatherjs['current']['pvdrWindSpd']))
    print('当前湿度：%s' % weatherjs['current']['rh'])
    print('当前空气污染物：')
    print('co:%s  no2:%s  o3:%s  pm2.5:%s  so2:%s'%(weatherjs['current']['co'], weatherjs['current']['no2'],
                                                    weatherjs['current']['o3'], weatherjs['current']['pm2.5'],
                                                    weatherjs['current']['so2']))
    print('当天天气信息：')
    print('更新时间：', weatherjs['forecast']['days'][0]['created'])
    print('当天天气：', weatherjs['forecast']['days'][0]['cap'])
    print('当天气温：%s℃(高) %s℃(低)'%(weatherjs['forecast']['days'][0]['tempHi'], weatherjs['forecast']['days'][0]['tempLo']))
    print('当天风向：%s\t风力：%s'%(weatherjs['forecast']['days'][0]['pvdrWindDir'], weatherjs['forecast']['days'][0]['pvdrWindSpd']))


def getForecastDaily(weatherjs):
    # print(weatherjs)
    for day in weatherjs['days']:
        print('#############################################')
        print('更新时间：', day['daily']['created'])
        print('预报时间：', day['daily']['valid'])
        print('当天气温：%s℃(高) %s℃(低)' % (day['daily']['tempHi'], day['daily']['tempLo']))
        print('白天天气：☀')
        print('当天天气：', day['daily']['day']['cap'])
        print('当天风向：%s\t风力：%s' % (day['daily']['day']['pvdrWindDir'], day['daily']['day']['pvdrWindSpd']))
        print('简介：', day['daily']['day']['summary'])
        print('夜间天气：☾')
        print('当天天气：', day['daily']['night']['cap'])
        print('当天风向：%s\t风力：%s' % (day['daily']['night']['pvdrWindDir'], day['daily']['night']['pvdrWindSpd']))
        print('简介：', day['daily']['night']['summary'])


def getAverage(weatherjs):
    pass


def getForecastTrend(weatherjs):
    pass


print('******************天气查询1.0******************')
address = getCityInfo(input('输入要查询城市：'))
if address is not None:
    cityInfo = {'lat': round(address['lat']+0.001,2),
                'lon': round(address['lon']+0.001,2)
                }
    getWeather(cityInfo, 'summary')
    getWeather(cityInfo, 'forecast_daily')
input('Press any key to exit.')
exit()

