from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
import socketio

# API resources and helpers
from apis.candlestick import CandleStickHandler
from helpers.db_helpers import process_resp_in_db

# app initialisation
app = Flask(__name__)
api = Api(app)
db = SQLAlchemy()
app.config[
    'SQLALCHEMY_DATABASE_URI'] = "postgres://eqslhnnfodvtbi:2c84f80f92b9575c53447f0d07dd052124a601aadc730d760e96c5e" \
                                 "764dd9ad8@ec2-34-193-232-231.compute-1.amazonaws.com:5432/d84ki3s7h5slp6"
db.init_app(app)

# API Routes
api.add_resource(CandleStickHandler, '/v1/getTradeData')

# socket connection
socketEndpoint = 'wss://stream.coindcx.com'
sio = socketio.Client()
sio.connect(socketEndpoint, transports='websocket')
sio.emit('join', {'channelName': 'I-BTC_INR'})
sio.wait()
print(sio)


@app.route('/')
def hello():
    return "CoinDCX Assignment!"


@sio.on('new-trade')
def on_message(response):
    if response.data:
        process_resp_in_db(response.data)


if __name__ == '__main__':
    app.run()
