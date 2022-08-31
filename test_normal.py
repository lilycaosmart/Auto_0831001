import requests
#import time
import re


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>API>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
washboard ="https://uniqa2-retail-vendor1.kiosoft.com:30008/"
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
    #time.sleep(3)
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
        #print(profile_data)
        total_len=int(profile_data[2:6],16)*2
        #print(total_len)
    else:
        print('API response have no data')
except Exception as e:
    print('API response analysis has error')

#判断除了83ff 还有的tag标记：total_len-83ff的长度-85的长度
if total_len<=526:
    res = hex(int((total_len - 5*2 - 4)/2))
    test = "83" + res[2:]
elif 526<=total_len<=1074:
    res = hex(int((total_len - 257*2 - 5*2 - 4)/2))
    test = "83" + res[2:]
elif 1074<total_len<1580:
    res = hex(int((total_len - 257 * 2*2 - 5 * 2 - 4) / 2))
    test = "83" + res[2:]
elif total_len>=1580:
    res = hex(int((total_len - 257 * 2 * 3 - 5 * 2 - 4) / 2))
    test = "83" + res[2:]
print(test)
#去掉前面2个block的数据
profile_data_array = profile_data[12:]



#去掉 83ff + 83** (83** 存在替换正常数据的风险）
profile_data = profile_data_array.replace("83ff","",)
profile_data = profile_data.replace(test,"")



#分block
profile_data_begin = profile_data.index('019999')
profile_data_end = profile_data.index('8502')
profile_data = profile_data[profile_data_begin:profile_data_end]
profile_data_array = re.findall(r'.{34}', profile_data)

print (profile_data_array)
# #去掉block号 并且整合为一个string
# list=[]
# str=""
# for s in profile_data_array:
#     s = s[2:]
#     str = str + s
#     #list.append(s)
#
# #去掉tag数
# str_ex_tagnumbers = str[2:]
#
# #切分tag
# while str_ex_tagnumbers:
#     m=int(str_ex_tagnumbers[2:4],16)*2
#     #print(str_ex_tagnumbers[2:4])
#     print(str_ex_tagnumbers[:m+4])
#     str_ex_tagnumbers = str_ex_tagnumbers[m+4:]


