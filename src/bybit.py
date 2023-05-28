import datetime
import os

from pybit.unified_trading import WebSocket
from time import sleep

old_best_bid = 0


def handle_message(message):
    global old_best_bid
    best_bid = message['data']['b'][0][0];

    if best_bid != old_best_bid:
        print(str(datetime.datetime.now()) + ": " + message['data']['b'][0][0])
        old_best_bid = best_bid


def main():
    ws = WebSocket(testnet=False, channel_type="linear", )
    ws.orderbook_stream(depth=1, symbol=os.environ['SYM_BYBIT'], callback=handle_message)
    while True:
        sleep(1)


if __name__ == '__main__':
    main()
