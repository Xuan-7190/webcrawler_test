import requests
from flask import Flask, request, render_template, redirect, url_for
from app_function import get_data_length, get_save_data_df, get_save_data_json, search_numbers_combination
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
        'hour' : '10',
        'minute' : '7',
        'second' : '30',
        'replace_existing' : True # 重新執行程序時，會將jobStore中的任務替換掉
    }]
    SCHEDULER_TIMEZONE = 'Asia/Taipei'  # 配置時區
    SCHEDULER_API_ENABLED = True  # 新增API


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

@app.route('/update', methods=['POST'])
def post_update():
    update_url = 'https://flask-lto-app.herokuapp.com/get_all_data'
    # update_url = 'http://127.0.0.1:5000/get_all_data'
    
    requests.get(update_url)
    
    return redirect(url_for('index'))
    

@app.route('/submit', methods=['POST'])
def post_submit():
    url = 'https://flask-lto-app.herokuapp.com/get_all_data/'
    # url = 'http://127.0.0.1:5000/get_all_data/'
    
    # 取得使用者選擇幾種數字組合
    combinations_list = request.form.get('combinations_list')
    # 取得輸入的數字組合
    number_str = ''
    for i in range(int(combinations_list)):
        if i != (int(combinations_list)-1):
            number_str += request.form.get('number'+str(i+1)) + ' '
        else:
            number_str += request.form.get('number'+str(i+1))
    # 取得輸入的期數範圍
    period = request.form.get('period')
    # 取得輸入的下幾期
    next = request.form.get('next')
    # 串接url
    if (period):
        # 有輸入期數
        search_url = url+'search_numbers='+number_str+'&period='+period+'&next='+next
    else:
        # 沒有輸入期數
        search_url = url+'search_numbers='+number_str+'&period='+str(get_data_length())+'&next='+next
    # 呼叫api
    response = requests.get(search_url)
    # 將結果轉成dic
    response_dic = response.json()
    # 將數字組合和結果組成list進行回傳
    data_list = [number_str, response_dic]
    # 顯示結果頁面
    return render_template('result.html', data=data_list)

@app.route('/search', methods=['POST'])
def post_search():
    search_url = 'https://flask-lto-app.herokuapp.com/get_save_data/'
    # search_url = 'http://127.0.0.1:5000/get_save_data/'
    
    # 取得輸入的期數範圍
    search_period = request.form.get('search_period')
    # 串接url
    if (search_period):
        # 有輸入期數
        search_url = search_url+'search_period='+search_period
    else:
        # 沒有輸入期數
        search_period = str(get_data_length())
        search_url = search_url+'search_period='+str(get_data_length())
    # 呼叫api
    response = requests.get(search_url)
    # 將結果轉成dic
    response_dic = response.json()
    # 將期數範圍和結果組成list進行回傳
    data_list = [search_period, response_dic]
    # 顯示結果頁面
    return render_template('search_result.html', data=data_list)

@app.route('/get_all_data')
def get_all_data_api():
    get_all_data()
    return 'update success'

@app.route('/get_save_data/search_period=<search_period>')
def get_save_data_api(search_period):
    return get_save_data_json(search_period)

@app.route('/search_numbers_combination/search_numbers=<search_numbers>&period=<period>', defaults={'next': 1})
@app.route('/search_numbers_combination/search_numbers=<search_numbers>&period=<period>&next=<next>')
def search_numbers_combination_api(search_numbers, period, next):
    return search_numbers_combination(search_numbers, period, next, get_save_data_df())

    # app.run(debug=True)