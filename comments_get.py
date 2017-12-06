import requests
import datetime
import time
import re
Token = '7bcbe786dc30553c097010cd323a82438b03a9570a1713e4386e254fac5cc292d2e110a74936f5fc2a1c8'

group_id = -15755094
post_id = 18211194
count = 100 #количество постов, получаемых за 1 запрос
offset = 0 #начальное смещение

#Узнаем сколько постов в сообществе

res = requests.get('https://api.vk.com/method/wall.getComments',
                     params={'owner_id': group_id, 'post_id': post_id, 'count': 100,
                             'need_likes': 1, 'offset': offset,
                             'access_token': Token})
comm_count = res.json()["response"][0]
print("Date", "User_id", "Text", "Likes")
while offset < comm_count:
    r = requests.get('https://api.vk.com/method/wall.getComments',
                     params={'owner_id': group_id, 'post_id': post_id, 'count': 100,
                             'need_likes': 1, 'offset': offset,
                             'access_token': Token})
    response = r.json()
    time.sleep(.33)
    for i in range(1, 101):
        post_date_unix = response['response'][i]['date']
        post_date = datetime.datetime.fromtimestamp(  # функция преобразования
            int(response['response'][i]['date'])).strftime('%Y-%m-%d')
        text = response['response'][i]['text']
        user_id = response['response'][i]['from_id']
        likes = response['response'][i]['likes']['count']
        print(str(post_date)+'^', str(user_id)+'^', str(text)+'^', str(likes))
    offset = offset + 100


