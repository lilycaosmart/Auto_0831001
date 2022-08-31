import requests
import time
import re


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>API>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
washboard ="https://uniqa2-amusement-vendor1.kiosoft.com:30008/"
#washboard="https://nicklaundry.kiosoft.com:5002/"
profile_id=input("pls input profile id:")

url = '%s/api' % washboard
headers = {'User-Agent': 'Mozilla/5.0'}

data = {
    'method': 'data',
    'profile_id': profile_id,
    'label_id': '33'
}
try:
    response = requests.post(url, headers=headers,data=data,verify=False)
    time.sleep(3)
# print(response.text)
# print(requests)
except Exception as e:
    print("response failed")
    print(e)
try:
    res_data = response.json()
except Exception as e:
    print('API response not json')

try:
    # res_data = response.json()
    if 'data' in res_data['result'].keys():
        profile_data = res_data['result']['data']
        total_len=int(profile_data[2:6],16)*2
        #去掉前面2个block的数据
        profile_data_array = profile_data[80:]
        #print(profile_data_array)
    else:
        print('API response have no data')
except Exception as e:
    print('API response analysis has error')

#判断除了83ff 还有的tag标记：



#去掉 83ff
profile_data = profile_data_array.replace("83ff","")




#分block
profile_data_begin = profile_data.index('50')
profile_data_end = profile_data.index('8e')
profile_data = profile_data[profile_data_begin:profile_data_end]
profile_data_array = re.findall(r'.{34}', profile_data)

#print("profile_data_array：",profile_data_array)

#去掉block号 并且整合为一个string
list=[]
str=""
for s in profile_data_array:
    s = s[2:]
    print(s)
    str = str + s
    #list.append(s)

#去掉tag数
str_ex_tagnumbers = str[2:]

#切分tag
while str_ex_tagnumbers:
    m=int(str_ex_tagnumbers[2:4],16)*2
    #print(str_ex_tagnumbers[2:4])
    print(str_ex_tagnumbers[:m+4])
    str_ex_tagnumbers = str_ex_tagnumbers[m+4:]


