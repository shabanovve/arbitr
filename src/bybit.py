import datetime

from src.common import handle_bybit

old_best_bid = 0


def handle_message(message):
    global old_best_bid
    best_bid = float(message['data']['b'][0][0])

    if best_bid != old_best_bid:
        print("bybit: " + str(datetime.datetime.now()) + ": " + message['data']['b'][0][0])
        old_best_bid = best_bid
        handle_bybit(best_bid)



