import requests
#import time
import re



# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>API>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
washboard ="https://uniqa2-retail-vendor1.kiosoft.com:30008/"
#washboard="https://nicklaundry.kiosoft.com:5002/"
profile_id=input("pls input profile id:")

test_0831 = { "STX":1,"Number of bytes":2}
res_test_0831={}

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
#print(test)
#去掉前面2个block的数据
profile_data_array = profile_data[80:]



#去掉 83ff + 83** (83** 存在替换正常数据的风险）
profile_data = profile_data_array.replace("83ff","",)
profile_data = profile_data.replace(test,"")



#分block
profile_data_begin = profile_data.index('04')
profile_data_end = profile_data.index('8502')
profile_data = profile_data[profile_data_begin:profile_data_end]
profile_data_array = re.findall(r'.{34}', profile_data)


for items in profile_data_array:
    print(items)

#去掉block号 并且整合为一个string
list=[]
str=""
for s in profile_data_array:
    s = s[2:]
    str = str + s
    #list.append(s)

#print(str)

#切分


test_ACA_TLW = { "Byte 0: STX":1,
              "Byte 1: Number of bytes in Data Field = 50":1,
              "Byte 2: Programming Data = 0x21 (TLW Prog)":1,
              "Byte 3: Product Byte #1 (byte checked by FEC, not programmed into FEC)":1,
              "Byte 4: Product Byte #2 (byte checked by FEC, not programmed into FEC)":1,
              "Byte 5: Product Byte #3 (byte checked by FEC, not programmed into FEC)":1,
              "Byte 6: unused":1,
              "Byte 7: unused":1,
              "Byte 8-9: Vend Price #1":2,
              "Byte 10-11: Vend Price #2":2,
              "Byte 12-13: Vend Price #3":2,
              "Byte 14-15: Vend Price #4":2,
              "Byte 16-17: Vend Price #5":2,
              "Byte 18-19: Vend Price #6":2,
              "Byte 20-21: Vend Price #7":2,
              "Byte 22-23: Vend Price #8":2,
              "Byte 24-25: Vend Price #9":2,
              "Byte 26-27: Cycle Modifier Key 1 Vend Price (Medium/B/Extra Wash)":2,
              "Byte 28-29: Cycle Modifier Key 2 Vend Price (Heavy/C/Extra Rinse)":2,
                 "Byte 32":1,
                 "Byte 33":1,
                 "Byte 34":1,
                 "Byte 35":1,
                 "Byte 36":1,
                 "Byte 37: Normal Extra Rinse Agitate Time":1,
                 "Byte 38: Normal Rinse Agitate Time":1,
                 "Byte 39: Normal Final Spin Time":1,
                 "Byte 40: Permanent Press Wash Agitate Time":1,
                 "Byte 41: Permanent Press Extra Rinse Agitate Time":1,
                 "Byte 42: Permanent Press Rinse Agitate Time":1,
                 "Byte 43: Permanent Press Final Spin Time":1,
                 "Byte 44: Delicate Wash Agitate Time":1,
                 "Byte 45: Delicate Extra Rinse Agitate Time":1,
                 "Byte 46: Delicate Rinse Agitate Time":1,
                 "Byte 47: Delicate Final Spin Time":1,
                 "Byte 48: Default Machine Cycle":1,
                 "Byte 49: Default Cycle Modifier":1,
                 "Byte 50: Warm Rinse":1,
                 "Byte 51: Audio Signal":1,
                 "Byte 52: BCC":1}
res_test_0831={}

for item in test_ACA_TLW:
    length_test = test_ACA_TLW[item]
    #print(int(length_test))
    res_test_0831[item] = str[:int(length_test)*2]
    str= str[length_test*2:]

#print(res_test_0831)
for item in res_test_0831:
    print("%s---->>: %s" %(item,res_test_0831[item]))

