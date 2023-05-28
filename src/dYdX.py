# Dependencies
import datetime
import os

import websocket, json, time
from sortedcontainers import SortedDict
from decimal import Decimal
from web3 import Web3
import pandas as pd

# dYdX dependencies
from dydx3 import Client
from dydx3.constants import *
from dydx3.constants import POSITION_STATUS_OPEN
from decimal import Decimal

from src.common import handle_dydx

ETHEREUM_ADDRESS = os.environ['ETHEREUM_ADDRESS']
private_client = Client(
    host='https://api.dydx.exchange',
    api_key_credentials={'key': os.environ['API_KEY'],
                         'secret': os.environ['API_SECRET'],
                         'passphrase': os.environ['PASS_PHRASE']},
    stark_private_key=os.environ['STARK_PRIVATE_KEY'],
    default_ethereum_address=ETHEREUM_ADDRESS,
)

account_response = private_client.private.get_account()
position_id = account_response.data['account']['positionId']

security_name = "NEAR-USD"  ##Change Market Pair Here
size = 1  ##Change Market size here
pct_spread = 0.1  ##Change spread charged here

dicts = {}
dicts['bids'] = {}  # bye
dicts['asks'] = {}  # sell

offsets = {}

skew = "buy"
bid_order_id = 0
ask_order_id = 0
position_balance_id = 0  # order id of postion clearing trade

old_best_bid = None;


def parse_message(msg_):
    global dicts, offsets

    if msg_["type"] == "subscribed":
        for side, data in msg_['contents'].items():
            for entry in data:
                size = Decimal(entry['size'])
                if size > 0:
                    price = Decimal(entry['price'])
                    dicts[str(side)][price] = size

                    offset = Decimal(entry["offset"])
                    offsets[price] = offset

    if msg_["type"] == "channel_data":
        # parse updates
        for side, data in msg_['contents'].items():
            if side == 'offset':
                offset = int(data)
                continue
            else:
                for entry in data:
                    price = Decimal(entry[0])
                    amount = Decimal(entry[1])

                    if price in offsets and offset <= offsets[price]:
                        continue

                    offsets[price] = offset
                    if amount == 0:
                        if price in dicts[side]:
                            del dicts[side][price]
                    else:
                        try:
                            dicts[side].append((price, amount))
                        except AttributeError:
                            dicts[side][price] = amount


def run_script():
    def on_open(ws):
        channel_data = {"type": "subscribe", "channel": "v3_orderbook", "id": str(security_name),
                        "includeOffsets": "True"}
        ws.send(json.dumps(channel_data))

    def on_message(ws, message):
        global dicts, skew, bid_order_id, ask_order_id, position_balance_id, position_id, old_best_bid

        obj = json.loads(message)
        parse_message(obj)

        best_bid = float(max(dicts["bids"].keys()))

        if best_bid != old_best_bid:
            print("dydx: " + str(datetime.datetime.now()) + ": " + str(best_bid))
            old_best_bid = best_bid
            handle_dydx(best_bid)

    def on_close(ws):
        print("### closed ###")

    socket = "wss://api.dydx.exchange/v3/ws"
    ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_close=on_close)
    ws.run_forever()

