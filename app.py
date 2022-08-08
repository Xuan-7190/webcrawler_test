import requests
import json
from flask import Flask, request, render_template, redirect
from app_function import get_data_length, get_save_data_top30_json, get_save_data_df, get_save_data_json, search_numbers_combination

url = 'https://flask-lto-app.herokuapp.com/search_numbers_combination/search_numbers='

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False # 讓傳出去的json可以中文顯示
app.config['JSON_SORT_KEYS'] = False # 輸出的json資料不要讓他排序

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def post_submit():
    # 取得輸入的數字組合
    number = request.form.get('number')
    # 串接url
    search_url = url+number
    # 呼叫api
    response = requests.get(search_url)
    print(type(response))
    # 將結果
    response_dic = response.json()
    print(type(response_dic))
    # print(response_dic['jdata'])
    print(response_dic['jdata'][0]['今彩539中獎號碼'])
    print(type(response_dic['jdata'][0]['今彩539中獎號碼']))
    # test_result = json.loads(str(response_dic['jdata'][0]))
    # print(test_result)
    
    return render_template('result.html', data=response_dic)

@app.route('/get_save_data_top30')
def get_save_data_top30_api():
    return get_save_data_top30_json()

@app.route('/get_save_data')
def get_save_data_api():
    return get_save_data_json()

@app.route('/search_numbers_combination/search_numbers=<search_numbers>', defaults={'period': get_data_length(), 'next': 1})
@app.route('/search_numbers_combination/search_numbers=<search_numbers>&period=<period>', defaults={'next': 1})
@app.route('/search_numbers_combination/search_numbers=<search_numbers>&next=<next>', defaults={'period': get_data_length()})
@app.route('/search_numbers_combination/search_numbers=<search_numbers>&period=<period>&next=<next>')
def search_numbers_combination_api(search_numbers, period, next):
    return search_numbers_combination(search_numbers, period, next, get_save_data_df())