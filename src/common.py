import functools
import logging
import threading
from datetime import datetime

from pandas import pandas as pd

log = logging.getLogger(__name__)

dydx_price = None
bybit_price = None
df = pd.DataFrame()


def synchronized(wrapped):
    lock = threading.Lock()

    @functools.wraps(wrapped)
    def _wrap(*args, **kwargs):
        with lock:
            result = wrapped(*args, **kwargs)
            return result

    return _wrap


@synchronized
def handle_dydx(price):
    global dydx_price
    dydx_price = price
    calculate()


@synchronized
def handle_bybit(price):
    global bybit_price
    bybit_price = price
    if (bybit_price is not None) & (dydx_price is not None):
        calculate()


def calculate():
    global df, dydx_price, bybit_price

    diff_price = bybit_price - dydx_price
    new_row = pd.DataFrame({'date': datetime.now(),
                            'bybit': bybit_price,
                            'dydx': dydx_price,
                            'diff': "{:.3f}".format(diff_price)}, index=[0])
    log.warning(str(new_row))

    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv('./share/diff.csv', index=False)
