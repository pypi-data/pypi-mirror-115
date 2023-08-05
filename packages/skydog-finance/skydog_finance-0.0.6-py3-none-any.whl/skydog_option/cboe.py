import requests

# expiry 2021-05-28


def get_option(underlying, strike, expiry, otype):
    import json
    from datetime import datetime

    url = "https://cdn.cboe.com/api/global/delayed_quotes/options/%s.json" % underlying.upper()
    print(url)

    headers = {
        # "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
        "referer": "https://www.cboe.com/"
    }

    response = requests.get(url, headers=headers)
    # print(response.text)
    json_data = json.loads(response.text)
    ticker_len = len(underlying)
    for opt in json_data["data"]["options"]:
        expiry_fmt = datetime.strptime(expiry, "%Y-%m-%d").strftime("%y%m%d")
        if expiry_fmt != opt["option"][ticker_len: ticker_len + 6]:
            continue
        if otype != opt["option"][ticker_len + 6]:
            continue
        strike_str = opt["option"][ticker_len + 7:]
        # print("strike=%f"%strike)
        # print(float(strike_str)/1000)
        if strike != int(strike_str) / 1000:
            continue
        # print(opt)
        dt = opt["last_trade_time"]
        opt["last_trade_date"] = dt[:10]
        opt["last_trade_time"] = dt[11:]
        return opt


def get_cboe_option_list(underlying, strike_range_percent, expiry_before, otype):
    import json
    from datetime import datetime

    url = "https://cdn.cboe.com/api/global/delayed_quotes/options/%s.json" % underlying
    print(url)

    headers = {
        # "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
        "referer": "https://www.cboe.com/"
    }

    response = requests.get(url, headers=headers)
    json_data = json.loads(response.text)
    ticker_len = len(underlying)
    result_list = []

    underlying_price_current = json_data["data"]["current_price"]

    if otype.upper() == "ALL":
        for opt in json_data["data"]["options"]:
            expiry_before_fmt = datetime.strptime(expiry_before, "%Y-%m-%d").strftime(
                "%y%m%d"
            )
            strike = int(opt["option"][ticker_len + 7:]) / 1000
            price_diff = strike - underlying_price_current
            strike_range = underlying_price_current * strike_range_percent / 100.0
            expiry_str = opt["option"][ticker_len: ticker_len + 6]
            otype_str = opt["option"][ticker_len + 6]

            if (
                expiry_before_fmt >= expiry_str
                and price_diff >= -strike_range
                and price_diff <= strike_range
            ):
                opt["strike"] = strike
                opt["expiry"] = datetime.strptime(expiry_str, "%y%m%d").strftime(
                    "%Y-%m-%d"
                )
                opt["otype"] = otype_str
                opt["premium_percent"] = opt["last_trade_price"] / strike
                result_list.append(opt)
    else:
        for opt in json_data["data"]["options"]:
            expiry_before_fmt = datetime.strptime(expiry_before, "%Y-%m-%d").strftime(
                "%y%m%d"
            )
            strike = int(opt["option"][ticker_len + 7:]) / 1000
            price_diff = strike - underlying_price_current
            strike_range = underlying_price_current * strike_range_percent / 100.0
            expiry_str = opt["option"][ticker_len: ticker_len + 6]
            otype_str = opt["option"][ticker_len + 6]

            if (
                expiry_before_fmt >= expiry_str
                and price_diff >= -strike_range
                and price_diff <= strike_range
                and otype_str == otype
            ):
                opt["strike"] = strike
                opt["expiry"] = datetime.strptime(expiry_str, "%y%m%d").strftime(
                    "%Y-%m-%d"
                )
                opt["otype"] = otype_str
                opt["premium_percent"] = opt["last_trade_price"] / strike
                result_list.append(opt)

    returned_data = {}
    returned_data["underlying"] = underlying
    returned_data["current_price"] = underlying_price_current
    returned_data["options"] = result_list
    return returned_data
