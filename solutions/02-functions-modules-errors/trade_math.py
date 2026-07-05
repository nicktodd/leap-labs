def trade_value(quantity, price):
    return quantity * price


def classify_trade(value, threshold=20000):
    if value > threshold:
        return "large"
    return "normal"
