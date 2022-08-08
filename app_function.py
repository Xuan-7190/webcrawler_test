import re
import pandas as pd
import json
from flask import jsonify

url = '''https://raw.githubusercontent.com/Xuan-7190/webcrawler_test/master/539%E6%A8%82%E9%80%8F%E8%B3%87%E6%96%99.csv'''

# 抓近30期的資料(回傳json格式)
def get_save_data_top30_json():
    # df = pd.read_csv('./539樂透資料.csv')
    df = pd.read_csv(url)
    df_top30 = df[:300]
    jdata = df_top30.to_json(orient='records', force_ascii=False)
    return jsonify(json.loads(jdata))


# 抓全部的資料(回傳df格式)
def get_save_data_df():
    # df = pd.read_csv('./539樂透資料.csv')
    df = pd.read_csv(url)
    return df


# 取得資料的全部範圍
def get_data_length():
    # df = pd.read_csv('./539樂透資料.csv')
    df = pd.read_csv(url)
    df_len = len(df)
    return df_len


# 抓全部的資料(回傳json格式)
def get_save_data_json():
    # df = pd.read_csv('./539樂透資料.csv')
    df = pd.read_csv(url)
    jdata = df.to_json(orient='records', force_ascii=False)
    return jsonify(json.loads(jdata))


# 處理資料的爛字串
def string_process(target_list_tmp):
    target_list_split = re.split(',|\[|\]| ', target_list_tmp)
    target_list = []
    for info in target_list_split:
        if info:
            target_list.append(info)
    return target_list


# 處理爛字串的list to int_list
def stringList_to_intList(input_list):
    output_list = []
    for i in input_list:
        output_list.append(int(i))
    return output_list

        
# 搜尋組合從限制期數的資料中及要顯示下幾期
def search_numbers_combination(search_numbers, period, next, lotto_all_data_df):
    try:
        lotto_all_data_df_tmp = lotto_all_data_df[:int(period)]
        
        source_list = stringList_to_intList(search_numbers.split())
        
        lotto_all_data_df_tmp['CK'] = False
        lotto_all_data_df_tmp['NEXT'] = False
        for i in range(len(lotto_all_data_df_tmp)):
            target_list = stringList_to_intList(string_process(lotto_all_data_df_tmp['今彩539中獎號碼'][i]))     

            # 判斷輸入的組合 有出現在這期 CK(check)=True
            check_count = 0
            for j in source_list:
                if j in target_list:
                    check_count+=1
            if check_count == len(source_list):
                lotto_all_data_df_tmp['CK'][i] = True
                lotto_all_data_df_tmp['CK'][i-int(next)] = True
                lotto_all_data_df_tmp['NEXT'][i-int(next)] = True

        # 不需要回傳 CK 欄位
        key_list = ['期數', '開獎日期', '今彩539中獎號碼', '備註']
        lotto_all_data_df = lotto_all_data_df_tmp[lotto_all_data_df_tmp['CK']==True]
        statistics_result = statistics_numbers(lotto_all_data_df_tmp[lotto_all_data_df_tmp['NEXT']==True][key_list])
        
        jdata = lotto_all_data_df[key_list].to_json(orient='records', force_ascii=False)
        
        payload = {
            'jdata': json.loads(jdata),
            'statistics_result': statistics_result
        }
        
        return jsonify(payload)
    
    except Exception as e:
        print(e)
        print('輸入格式錯誤')
        
        
# 統計號碼出現的次數
def statistics_numbers(df):
    target_dict = {}
    for index, value in enumerate(df['今彩539中獎號碼']):
        
        target_list_split = re.split(',|\[|\]| ', value)
        
        for info in target_list_split:
            if info:
                target_dict[int(info)] = target_dict.get(int(info), 0) + 1
                
    target_dict_bykey = {k: v for k, v in sorted(target_dict.items(), key=lambda item: item[0])}
    target_dict_byvalue = {k: v for k, v in sorted(target_dict_bykey.items(), key=lambda item: item[1], reverse=True)}
    return target_dict_byvalue