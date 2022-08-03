import requests
from bs4 import BeautifulSoup
# from lxml import etree, html
import re
import pandas as pd


# 處理資料的爛字串
def lotto_data_process(lotto_table_info):
    # ['', '4664', '2022/07/23', '05\xa0,\xa027\xa0\xa032\xa0,\xa033\xa0,\xa038\xa0', '', '無', '']
    # -> ['', '4664', '2022/07/23', '05', '', '', '27', '', '32', '', '', '33', '', '', '38', '', '', '無', '']
    lotto_table_info_data = re.split(',|\n|\xa0', lotto_table_info)
    
    # ['', '4664', '2022/07/23', '05', '', '', '27', '', '32', '', '', '33', '', '', '38', '', '', '無', '']
    # -> ['4664', '2022/07/23', '05', '27', '32', '33', '38', '無']
    new_lotto_table_info_data = []
    for info in lotto_table_info_data:
        if info:
            new_lotto_table_info_data.append(info)
    
    # print(new_lotto_table_info_data)
    return new_lotto_table_info_data


def get_all_data():
    
    # 第一次進來先抓所有頁數
    first_url = f'https://www.pilio.idv.tw/lto539/listBBK.asp'

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }

    res = requests.get(first_url, headers=headers)
    # 轉換編碼至big5
    res.encoding = 'big5'
    soup = BeautifulSoup(res.text, 'lxml')

    # 抓出所有連結 因為要其他頁的資料
    lotto_numbers_info = soup.find_all('a')
    # 抓出所有的頁數 index 21開始第一頁 index len-7最後一頁
    total_page = []
    for i in range(21, len(lotto_numbers_info)-7):
        total_page.append(lotto_numbers_info[i].text)

    # 所有樂透資料的list
    lotto_table_info_all = []
    # 取得所有頁數的樂透資料
    for i in total_page:
        url = f'https://www.pilio.idv.tw/lto539/listbbk.asp?indexpage={i}&orderby=new'
        res = requests.get(url, headers=headers)
        # 轉換編碼至big5
        res.encoding = 'big5'
        soup = BeautifulSoup(res.text, 'lxml')

        # 因為資料在表格的tr 沒有id
        lotto_table_info = soup.find_all('tr')

        # 樂透資料從index 2 ~ index len-1
        for i in range(2, len(lotto_table_info)-1):
            lotto_table_info_all.append(lotto_data_process(lotto_table_info[i].text))
    
    # 變成 dataframe 後續計算可能比較方便
    df_tmp = pd.DataFrame(lotto_table_info_all, columns=['期數', '開獎日期', '2', '3', '4', '5', '6', '備註'])
    # 字元轉整數  避免小錯誤
    df_tmp['2'] = df_tmp['2'].astype(int)
    df_tmp['3'] = df_tmp['3'].astype(int)
    df_tmp['4'] = df_tmp['4'].astype(int)
    df_tmp['5'] = df_tmp['5'].astype(int)
    df_tmp['6'] = df_tmp['6'].astype(int)
    key_list = ['2', '3', '4', '5', '6']
    df_tmp['今彩539中獎號碼'] = df_tmp[key_list].values.tolist()
    df_columns = ['期數', '開獎日期', '今彩539中獎號碼', '備註']
    df = df_tmp[df_columns]
    
    df.to_csv('539樂透資料.csv', encoding='utf-8', index=False)


print('start')
get_all_data()
print('done!')