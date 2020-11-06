import os
from flask import Flask, jsonify, render_template, url_for, request, redirect
# url_for : 해당 지점으로 향하는 url을 만들어주는 함수?
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from webCrawl.crawling import search
from AI import classifier
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from tensorflow import keras
from flask_apscheduler import APScheduler
import numpy as np
import pandas as pd
import pickle

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # /// 세개는 상대적 path, //// 네개는 절대 path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)

model = keras.models.load_model(basedir+'/AI/my_model.h5')
with open(basedir+'/AI/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

class Config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': 'app:refineModel',
            'args': (8000,5000),
            'trigger': 'interval',
            # 'seconds': 5,
            'hours': 168
        }
    ]

    SCHEDULER_API_ENABLED = True

def refineModel(min_num,interval_num):
    print('model refining')
    # with open(basedir+'/AI/DataInfo.txt','r') as f:
    #     beforeNum = int(f.read())
    # data = pd.read_csv('data.csv',encoding='utf-8')
    # data.drop_duplicates(subset=['content'], inplace=True) 
    # nowNum = len(data)
    # with open(basedir+'../AI/DataInfo.txt','w') as f:
    #     f.write(nowNum)
    # if (nowNum > int(min_num) and nowNum - beforeNum >= int(interval_num)):
    #     classifier.createModel()

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    user = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(30), nullable=False)
    price = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    date = db.Column(db.String(25), nullable=False)
    url = db.Column(db.String(100), nullable=False)
    report = db.Column(db.String(5), nullable=False)

    def __repr__(self):
        return f'<Transaction {self.id}>'

@app.route('/', methods=['GET'])
def test():
    return "flask Sever is On"

@app.route('/report', methods=['POST'])
def report():
    if request.method=='POST':
        # will change later
        request_data = request.json
        content = ' '.join(request_data.get("content"))
        try:
            Exis = Transaction.query.filter_by(url=request_data.get('url')).first()
            if not Exis:
                new_transaction = Transaction(
                    title=request_data.get('title'),
                    user=request_data.get('user'),
                    category=request_data.get('category'),
                    price=request_data.get('price'),
                    content=content,
                    date=request_data.get('date'),
                    url=request_data.get('url'),
                    report=request_data.get('report'),
                )
                db.session.add(new_transaction)
                db.session.commit()
                with open(basedir + '/AI/data.csv', 'a', encoding='utf8') as f:
                    if (request_data.get('report')=='1'):
                        f.write(f'1,{content},"{request_data.get("price")}"\n')
                    elif (request_data.get('report')=='2'):
                        f.write(f'0,{content},"{request_data.get("price")}"\n')
                if (request_data.get('report')=='3'):
                     with open(basedir + '/needToCheck.csv', 'a', encoding='utf8') as f:
                        f.write(f'{request_data.get("title")},{request_data.get("user")},{content},"{request_data.get("price")}",{request_data.get("url")}\n')
                return {
                    "status": 200,
                    "message" : f"transaction {new_transaction.id} {new_transaction.report} has been successfully reported"
                }
            else:
                return {
                    "status" : 404,
                    "message": "already reported"
                }
            
        except Exception as e:
            print(str(e))
            return f"error! {str(e)}"
    else:
        return "wrong method"


@app.route('/search/<int:menu>/<string:keyword>/<int:page>', methods=['GET'])
def process(menu, keyword, page):
    try:
        if request.method == "GET":
            # print("start searching")
            original = search(menu,keyword, page)
            x_data = []
            for datum in original:
                if datum['content']:
                    x_data.append(' '.join(datum['content']))
                else:
                    x_data.append(datum['title'])

            # print('MAKE SEQUENCE')
            sequences = tokenizer.texts_to_sequences(x_data)
            x_data = sequences
            # print('data processing')
            max_len = max(len(l) for l in x_data)
            data = np.array(pad_sequences(x_data, maxlen = max_len))
            # print('predict')
            result = model.predict(data)
            resultlist = result.tolist()
            
            for idx in range(len((original))):
                original[idx]['isTrader'] = resultlist[idx][0] 
            return jsonify(original)
    except Exception as e:
        print(str(e))
    return "OMG, Something Wrong"

if __name__ == "__main__":

    app.config.from_object(Config())

    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    app.run(debug=False, host="0.0.0.0", port=5000)