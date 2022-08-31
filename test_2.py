import requests
import time
import re


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>API>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
washboard ="https://uniqa2-retail-vendor2.kiosoft.com:30008"
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
        print(profile_data)
        if len(profile_data)>1000:
            profile_data_begin_1 = profile_data.index('50')
            profile_data_end_1 = profile_data.index('8e')
            profile_data_1 = profile_data[profile_data_begin_1:profile_data_end_1]
            profile_data_array = re.findall(r'.{34}', profile_data_1)

            # profile_data_begin_2 = profile_data.index('5d')
            # profile_data_end_2 = profile_data.index('6c')
            # profile_data_2 = profile_data[profile_data_begin_2:profile_data_end_2]
            # profile_data_array_2 = re.findall(r'.{34}', profile_data_2)
            #
            # profile_data_begin_3 = profile_data.index('6c')
            # profile_data_end_3 = profile_data.index('8e')
            # profile_data_3 = profile_data[profile_data_begin_3:profile_data_end_3]
            # profile_data_array_3 = re.findall(r'.{34}', profile_data_3)

            #profile_data_array = profile_data_array_1+profile_data_array_2+profile_data_array_3
        elif len(profile_data)<1000:
            profile_data_begin_1 = profile_data.index('50')
            profile_data_end_1 = profile_data.index('8e')
            profile_data_1 = profile_data[profile_data_begin_1:profile_data_end_1]
            profile_data_array = re.findall(r'.{34}', profile_data_1)

            # profile_data_begin_2 = profile_data.index('5d')
            # profile_data_end_2 = profile_data.index('8e')
            # profile_data_2 = profile_data[profile_data_begin_2:profile_data_end_2]
            # profile_data_array_2 = re.findall(r'.{34}', profile_data_2)
            #
            # profile_data_array = profile_data_array_1 + profile_data_array_2


    else:
        print('API response have no data')
except Exception as e:
    print('API response analysis has error')
print(profile_data_array)

#去掉block号 并且整合为一个string
list=[]
str=""
for s in profile_data_array:
    s = s[2:]
    str = str + s
    #list.append(s)
str_ex_tagnumbers = str[2:]
#print("str_ex_tagnumbers=",str_ex_tagnumbers)

#切分tag
while str_ex_tagnumbers:
    m=int(str_ex_tagnumbers[2:4],16)*2
    print(str_ex_tagnumbers[:m+4])
    str_ex_tagnumbers = str_ex_tagnumbers[m+4:]


