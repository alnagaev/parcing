import requests
import pandas as pd

token = open('C:/Users/USER/Documents/token.txt', 'r').read()

owner_id = input()

def get_members(owner_id):
    from collections import defaultdict
    s = defaultdict(list)
    r = requests.post('https://api.vk.com/method/execute.groupMembers?group_id='+
                      str(owner_id)+'&offset='+str(0)+'&v='+'5.73'+'&count='+str(5000)
                      +'&access_token='+token).json()['response']
    ##################################################################################
    members_count = r[0] #количество участников
    print('В сообществе', owner_id, 'участников :',members_count)
    for k,v in r[1][0].items():
        s[k].extend(v)

    if members_count>5000:
        for offset in range(5000, members_count, 5000):
            try:
                count = offset + 5000
                r = requests.post('https://api.vk.com/method/execute.groupMembers?group_id='+
                                 str(owner_id)+'&offset='+str(offset)+'&v='+'5.73'+'&count='+
                                 str(count)+'&access_token='+token).json()['response'][1][0]
                for k,v in r.items():
                    s[k].extend(v)
            except Exception:
                pass

    return s

result = get_members(owner_id)
df_1 = pd.DataFrame.from_dict(result)

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
