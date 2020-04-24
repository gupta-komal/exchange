import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
db = SQLAlchemy()


def normalised_response(result_object):
    decoded_response = []
    for row in result_object:
        decoded_response.append(dict(row))
    return decoded_response


def process_resp_in_db(data):

    """
    :param data: Received data from coinDCX event
    :return:
    """
    data = data.json()
    event_query_params = ({
        'price': data.get('p'),
        'quantity': data.get('q'),
        'symbol': data.get('s'),
        'ts': data.get('T'),
        'is_market': data.get('m')
    })
    event_query = text(
        "insert into tradeData (price, quantity, symbol, ts, is_market) values "
        "(:price, :quantity, :symbol, :ts, :is_market)")
    db.engine.execute(event_query, event_query_params)
