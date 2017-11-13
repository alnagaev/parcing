import requests, time, datetime, re
Token = '7bcbe786dc30553c097010cd323a82438b03a9570a1713e4386e254fac5cc292d2e110a74936f5fc2a1c8'
id_list = []
name_list = []
offset = 0
owner = '-146824594'
post = '330'
# owner = input('ВВИДИТИ ОВНЕРА(помните, что в начале должен быть минус):' )
# post = input('ВВИДИТИ НОМЕР:')
res = requests.get('https://api.vk.com/method/wall.getById', params = {'posts':owner+'_'+post, 'acces_token': Token})
count = res.json()['response'][0]['reposts']['count']

while offset < count:
    r = requests.get('https://api.vk.com/method/wall.getReposts', params={'owner_id':owner, 'post_id': post,
                                                                          'count': 1000, 'offset': offset, 'access_token':Token})
    response = r.json()
    groups = response['response']['groups']
    for i in range(0, len(groups)):
        gid = -(groups[i]['gid'])
        id_list.append(gid)
        name = groups[i]['name']
        name_list.append(name)
    offset = offset + 10

# Делаем словарь из названий групп в качестве ключей и id в качестве значений
def uniqList():
    b = []
    c = []
    dict_ = {}
    for el in id_list:
        if el in id_list and el not in b:
            b.append(el)
    for el in name_list:
        if el in name_list and el not in c:
            c.append(el)
    for x, y in zip(c, b):
        dict_[x] = y
    return dict_

list_values = list(uniqList().values())
list_keys = list(uniqList().keys())
#тупо, но надо вернуть список из значений и ключей , который был получен из функции

#Считаем количество постов в группах. Как для общего развития, так и для дальнейшей работы.
def postCount(group):
    r = requests.get('https://api.vk.com/method/wall.get',
                     params={'owner_id': group, 'count': 0, 'access_token': Token})
    time.sleep(.33)
    try:
        post_count = r.json()["response"][0]  # количество постов в группе или профиле
    except Exception:
        post_count = 'Group is closed or deleted or some other error occurred'
    return post_count

pstcount = []
for i in list_values:
    pstcount.append(postCount(i))

def dict_pst():
    dict_ = {}
    for x, y, z in zip(list_keys, list_values, pstcount):
        dict_[x] = y, z
    return dict_



def postDownload(group, count_):
    global likes_count
    offset = 0
    if count_ != 'Group is closed or deleted or some other error occurred':
        while offset < count_:
            r = requests.get('https://api.vk.com/method/wall.get',
                             params={'owner_id': group, 'count': 100, 'offset': offset, 'access_token': Token})
            time.sleep(.33)
            for post_ in range(1, 101):
                try:
                    post_date_unix = r.json()['response'][post_]['date']
                    likes_count = r.json()['response'][post_]['likes']['count']
                except Exception:
                    likes_count = None
                offset = offset + 100
                print(str(group)+' '+str(likes_count))

            if post_date_unix > 1508716800:  # 1 марта = 1488326400
                continue
            else:
                break
    else:
        print('Closed group, no data')


for x, y in zip(list_values, pstcount):
    print(str(postDownload(x, y)))

print("It's over")
