* When I use `pycharm` to rename module `types.prices.py` to `types.localised_prices.py`, `dmypy` gets confused and it started to report false negative results. 

```python
happymoose/models/orders.py:1006: error: Argument 2 to "adjust_credit" of "Customer" has incompatible type "happymoose.types.localised_prices.LocalisedPrice"; expected "happymoose.types.prices.LocalisedPrice"
```

All I needed was to restart `dmypy` through `dmypy restart`
