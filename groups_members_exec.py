import requests
import time as t
import pprint, codecs
import pandas as pd

token = open('C:/Users/USER/Documents/token.txt', 'r').read()


def get_members_list_id(owner_id):
    members_list = []  # изначально пустой список участников

    # первый запрос на 25000, чтобы получить первые 25000 и количество участников группы
    r = requests.post('https://api.vk.com/method/execute.grpFull?group_id=' +
                      str(owner_id) + '&offset=' + str(0) + '&count=' + str(25000) + '&access_token=' + token).json()[
        'response']
    members_count = r[0]  # количество участников

    print('В сообществе', owner_id, 'участников :', members_count)

    members_list.extend(r[1])  # вносим первые 25000 ID

    if members_count > 25000:
        for offset in range(25000, members_count, 25000):
            count = offset + 25000

            r = requests.post('https://api.vk.com/method/execute.grpFull?group_id=' +
                              str(owner_id) + '&offset=' + str(offset) + '&count=' + str(
                count) + '&access_token=' + token).json()['response']

            members_list.extend(r[1])  # вносим все последующие ID пачками по 25000 ID

            # t.sleep(.35) #задержки между запросом --- ВАЖНО: если будут возникать проблемы - расскоментировать
        print('Done')
    else:
        print('Less than 25000')

    return members_list


users_data = get_members_list_id(int(input('Input group ID: ')))


def data_cleaning():
    "Создаем словарь, который можно будет превратить в py файл или в эксель файл, как пожелаете"
    members_dict = {}

    sexl, bdatel, cityl = [], [], []
    uid = [users_data[i]['id'] for i in range(len(users_data))]
    first_name = [users_data[i]['first_name'] for i in range(len(users_data))]
    last_name = [users_data[i]['last_name'] for i in range(len(users_data))]
    for i in range(len(users_data)):
        try:
            sex = users_data[i]['sex']
        except Exception:
            sex = 0
        sexl.append(sex)

        try:
            bdate = users_data[i]['bdate']
        except Exception:
            bdate = 0
        bdatel.append(bdate)

        try:
            city = users_data[i]['city']['title']
        except Exception:
            city = 0
        cityl.append(city)

    members_dict = {'id': uid, 'first_name': first_name, 'last_name': last_name, 'sex': sexl,
                    'bdate': bdatel, 'city': cityl}

    print('Done')
    return members_dict


df_1 = pd.DataFrame.from_dict(data_cleaning())


def write_excel(df):
    # Функция для записи датафрейма в эксель
    try:
        writer = pd.ExcelWriter('{}.xlsx'.format(input('Input file_name: ')))
        df.to_excel(writer, 'Sheet1')
        writer.save()
        print('Файл записан')
    except Exception as e:
        print(str(e))


write_excel(df_1)