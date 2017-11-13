# -*- coding: utf-8 -*-
import urllib
import urllib2
import json

handler = urllib2.HTTPHandler()
opener = urllib2.build_opener(handler)

def get_links(jsondata):
    links = []
    try:
        c = 0
        while True:
            links.append(jsondata['posts'][c]['main_image_url'])
            c+=1
    except:
        pass
    return links


def rq(url, values, headers, method):
    if values!= False:
        data = urllib.urlencode(values)
        request = urllib2.Request(url, data=data, headers=headers)
    else:
        request = urllib2.Request(url, headers=headers)
    request.get_method = lambda: method
    connection = opener.open(request)
    resp = str(connection.read())
    jsondata = json.loads(resp)
    return jsondata

username = raw_input('username: ')
password = raw_input('password: ')
values = {'username' : username,
          'password' : password,
          }
headers = {"Content-Type": "application/x-www-form-urlencoded"}

jsondata = rq('https://d3.ru/api/auth/login/', values, headers, 'POST')
uid = jsondata[u'uid']
sid = jsondata[u'sid']
print 'User ID: ' + uid + ' Session ID: ' + sid
headers = {'X-Futuware-UID' : uid,
           'X-Futuware-SID' : sid,
           'Content-Type':'application/json',
          }

jsondata = rq('https://d3.ru/api/users/' + username + '/favourites/posts/', False, headers, 'GET')

item_count = jsondata['item_count']

url_list = []

if item_count > 42:
    page_num = 1
    while page_num*42 < item_count+42:
        jsondata = rq('https://d3.ru/api/users/' + username + '/favourites/posts/?page=' + str(page_num), False, headers, 'GET')
        current_list = get_links(jsondata)
        url_list = url_list + current_list
        page_num += 1
else:
     jsondata = rq('https://d3.ru/api/users/' + username + '/favourites/posts/?page=1', False, headers, 'GET')
     url_list = get_links(jsondata)

img_num = 1

print u'У Вас (примерно...) ' + str(len(url_list)) + u' картинок.'
print u'Сохраняю...'
for link in url_list:
    urllib.urlretrieve(link, u'Картинка ' + str(img_num) + '.jpeg')
    img_num+=1

print u'Готово'
