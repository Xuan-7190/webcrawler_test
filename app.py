from flask import Flask
from app_function import get_data_length, get_save_data_top30_json, get_save_data_df, get_save_data_json, search_numbers_combination
import time

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False # 讓傳出去的json可以中文顯示
app.config['JSON_SORT_KEYS'] = False # 輸出的json資料不要讓他排序

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