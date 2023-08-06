# EasyIB: Unofficial Wrapper for Interactive Brokers API
[![](https://img.shields.io/pypi/v/easyib.svg)](https://pypi.org/pypi/easyib/)
[![](https://img.shields.io/pypi/pyversions/easyib.svg)](https://pypi.org/pypi/easyib/)
[![](https://img.shields.io/pypi/l/easyib.svg)](https://pypi.org/pypi/easyib/)

EasyIB is an unofficial python wrapper for [Interactive Brokers Client Portal Web API](https://interactivebrokers.github.io/cpwebapi/).
Notable functionality includes:
- Pull account info, portfolio, cash balance, net value
- Pull market historical data
- Submit, modify, cancel orders
- Get order status, list of live orders
- Ping (tickle) server, get authentication status, re-authenticate

# How to Install
```
pip install easyib
```
EasyIB assumes a gateway session is active and authenticated.
Follow instructions at https://interactivebrokers.github.io/cpwebapi/ for authentication.
A custom package such as [Voyz/IBeam](https://github.com/voyz/ibeam) can be also used for setting up an active session.

# Quick start

### Historical Data
```python
import easyib

api = easyib.REST()
# By default, easyib assumes the gateway session is at local port 5000 without a ssl certificate
# A custom port may be set by `api = easyib.REST(url="https://localhost:5000", ssl=False)`

bars = api.get_bars("AAPL", period="1w", bar="1d")
print(bars)
```


### Submitting an order
```python
list_of_orders = [
    {
        "conid": api.get_conid("AAPL"),
        "orderType": "MKT",
        "side": "BUY",
        "quantity": 7,
        "tif": "GTC",
    }
]
# For order parameters, see 'order request info' at https://www.interactivebrokers.com/api/doc.html#tag/Order/paths/~1iserver~1account~1{accountId}~1orders/post

api.submit_orders(list_of_orders)
```
