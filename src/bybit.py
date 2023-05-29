from src.common import handle_bybit

old_best_bid = 0


def handle_message(message):
    global old_best_bid
    best_bid = float(message['data']['b'][2][0])

    if best_bid != old_best_bid:
        old_best_bid = best_bid
        handle_bybit(best_bid)
