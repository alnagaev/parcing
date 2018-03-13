import requests
import datetime
import pandas as pd
from collections import defaultdict


s = defaultdict(list)
token = open('C:/Users/USER/Documents/token.txt', 'r').read()

owner_id = input()

def get_members_list_id(owner_id):
    cnt = requests.post('https://api.vk.com/method/execute.postcount?id='+
                      str(owner_id)+'&offset='+str(0)+'&v='+'5.73'+
                      '&access_token='+token).json()['response']

    r = requests.post('https://api.vk.com/method/execute.wallGet?id='+
                      str(owner_id)+'&offset='+str(0)+'&v='+'5.73'+
                      '&access_token='+token).json()['response']

    return r


result = get_members_list_id(owner_id)

for i in range(len(result)):
    for k, v in result[i].items():
        s[k].extend(v)

date = []
for i in s['dates']:
    date.append(datetime.datetime.fromtimestamp(i).strftime('%Y-%m-%d'))

s['dates'] = date

df_1 = pd.DataFrame.from_dict(s)

def write_excel(df):
    #Функция для записи датафрейма в эксель
    try:
        writer = pd.ExcelWriter('{}.xlsx'.format(input('Input file_name: ')))
        df.to_excel(writer,'Sheet1')
        writer.save()
        print('Файл записан')
    except Exception as e:
        print(str(e))

write_excel(df_1)
