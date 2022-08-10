import pandas as pd
import json
from flask import jsonify
import re
import requests

# df = pd.read_csv('./539樂透資料.csv')
# df_top30 = df[:30]
# print(type(df_top30['今彩539中獎號碼'][0]))

# df_top30['今彩539中獎號碼'] = df_top30['今彩539中獎號碼'].map(lambda x: re.split(',|\[|\]| ', x))

# print(df_top30['今彩539中獎號碼'])

response = requests.get('http://127.0.0.1:5000/get_save_data')
response_dic = response.json()
# for i in range(len(response_dic)):
#     print(response_dic[i].get('今彩539中獎號碼'))
#     print(type(response_dic[i].get('今彩539中獎號碼')))

print(response_dic[0].get('今彩539中獎號碼'))
print(type(response_dic[0].get('今彩539中獎號碼')))
print(list(response_dic[0].get('今彩539中獎號碼')))

# string = '[9, 11, 31, 36, 39]'

# source_list = re.split(',|\[|\]| ', string)
# # print(source_list)

# target_list = []
# for info in source_list:
#     if info and len(info)==1:
#         target_list.append('0'+info)
#     elif info:
#         target_list.append(info)

# print(target_list)
