# -*- coding: utf-8 -*-

import importlib
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
importlib.reload(sys)

from celery import current_app as app
from app.tasks import CustomerTask


# 更新币价
@app.task(name="market_price", base=CustomerTask, exchange="statistic")
def market_price():
    pass
