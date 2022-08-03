from flask import Flask
from app_function import get_save_data_top30_json, get_save_data_df, get_save_data_json, search_numbers_combination, search_numbers_combination_limited


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False # 讓傳出去的json可以中文顯示
@app.route('/get_save_data_top30')
def get_save_data_top30_api():
    return get_save_data_top30_json()

@app.route('/get_save_data')
def get_save_data_api():
    return get_save_data_json()

@app.route('/search_numbers_combination/search_numbers=<search_numbers>')
def search_numbers_combination_api(search_numbers):
    return search_numbers_combination(search_numbers, get_save_data_df())

@app.route('/search_numbers_combination_limited/period=<period>&search_numbers=<search_numbers>')
def search_numbers_combination_limited_api(period, search_numbers):
    return search_numbers_combination_limited(period, search_numbers, get_save_data_df())