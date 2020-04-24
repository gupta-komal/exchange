import datetime as DT
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource
from sqlalchemy import text

from helpers.db_helpers import normalised_response

db = SQLAlchemy()


class CandleStickHandler(Resource):

    def get(self):
        """
         Gives trade data from database
         accepts the timeline value from query param though the default is current day
        :return:
        """
        resp = {"status": 1, "desc": ""}
        tl = request.args.get("tl")
        today = DT.datetime.today()
        ts = (today - DT.timedelta(days=1)).timestamp()
        if tl and tl.upper() == '1W':
            target_date = today - DT.timedelta(days=7)
            ts = target_date.timestamp()

        elif tl and tl.upper() == 'FN':
            target_date = today - DT.timedelta(days=15)
            ts = target_date.timestamp()

        elif tl and tl.upper() == '1M':
            target_date = today - DT.timedelta(days=30)
            ts = target_date.timestamp()
        elif tl and tl.upper() == 'ALL':
            ts = None
        if ts:
            nq = text(
                "select price as p, quantity as q, ts as T, symbol as s, is_market as m from tradeData where ts>:ts")
            nr = normalised_response(db.engine.execute(nq, ({'ts': str(ts)})))
        else:
            nq = text(
                "select price as p, quantity as q, ts as T, symbol as s, is_market as m from tradeData")
            nr = normalised_response(db.engine.execute(nq))
        if not nr:
            resp['status'] = 0
            resp['desc'] = 'No Data Found'
        resp ['data'] = nr
        return resp