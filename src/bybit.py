from pybit.unified_trading import WebSocket
from time import sleep


def handle_message(message):
    print(message)


def main():
    ws = WebSocket(testnet=False, channel_type="linear",)
    ws.orderbook_stream(depth=50, symbol="BTCUSDT", callback=handle_message)
    while True:
        sleep(1)


if __name__ == '__main__':
    main()
