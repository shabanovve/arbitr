import os
from asyncio import sleep
from pybit.unified_trading import WebSocket
from src.bybit import handle_message
from src.dYdX import run_script


def main():
    if not os.path.exists('./share'):
        raise Exception('share does not exist')

    ws = WebSocket(testnet=False, channel_type="linear", )
    ws.orderbook_stream(depth=1, symbol=os.environ['SYM_BYBIT'], callback=handle_message)

    run_script()

    while True:
        sleep(1)


if __name__ == '__main__':
    main()