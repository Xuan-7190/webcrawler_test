import requests
from flask import Flask, request, render_template
from app_function import get_data_length, get_save_data_top30_json, get_save_data_df, get_save_data_json, search_numbers_combination
from apscheduler.schedulers.background import BackgroundScheduler
from flask_apscheduler import APScheduler
from get_all_data import get_all_data



class Config(object):
    # JOBS可以在配置裡面配置
    JOBS = [{
        'id': 'job1',
        'func': 'app:get_all_data',
        'trigger' : 'cron',
        'day' : '*',
        'hour' : '21',
        'minute' : '0',
        'second' : '0',
        'replace_existing' : True # 重新執行程序時，會將jobStore中的任務替換掉
    }]
    SCHEDULER_TIMEZONE = 'Asia/Taipei'  # 配置時區
    SCHEDULER_API_ENABLED = True  # 新增API

url = 'https://flask-lto-app.herokuapp.com/search_numbers_combination/'

# if __name__ == "__main__":
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False # 讓傳出去的json可以中文顯示
app.config['JSON_SORT_KEYS'] = False # 輸出的json資料不要讓他排序

# 初始化排程器
scheduler = APScheduler(BackgroundScheduler(timezone="Asia/Taipei"))
app.config.from_object(Config())
scheduler.init_app(app)
scheduler.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def post_submit():
    # 取得使用者選擇幾種數字組合
    combinations_list = request.form.get('combinations_list')
    # 取得輸入的數字組合
    number_str = ''
    for i in range(int(combinations_list)):
        number_str += request.form.get('number'+str(i+1)) + ' '
        # number = request.form.get('number')
    # 取得輸入的期數範圍
    period = request.form.get('period')
    # 取得輸入的下幾期
    next = request.form.get('next')
    # 串接url
    if (not period):
        search_url = url+'search_numbers='+number_str+'&next='+next
    elif period:
        search_url = url+'search_numbers='+number_str+'&period='+period+'&next='+next
    # 呼叫api
    response = requests.get(search_url)
    # 將結果轉成dic
    response_dic = response.json()
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
   
    # app.run(debug=True)