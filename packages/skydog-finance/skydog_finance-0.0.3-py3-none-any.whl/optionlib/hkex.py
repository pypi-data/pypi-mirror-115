import re
import requests
from lxml import html
from bs4 import BeautifulSoup

# underlying must be 5-digital number, such as 00700


def current(underlying, strike, expiry, otype):
    """
    underlying: underlying security ticker
    strike: strike price
    mdate: mature date
    otype: C for Call, P for Put
    """
    if underlying[-3:].lower() == ".hk":
        underlying = underlying[:-3]
    while len(underlying) < 5:
        underlying = "0" + underlying
    url = "https://www.hkex.com.hk/eng/sorc/options/stock_options_detail.aspx"
    request_data = {
        "action": "ajax",
        "type": "list",
        "otype": otype,
        "underlying": underlying,
        "expiry": expiry,
        "strike": strike,
        "page": 1,
    }
    # print(request_data)
    option_list_res = requests.post(url, data=request_data)
    dom = html.fromstring(option_list_res.text)
    # print(option_list_res.text)
    # return
    href = dom.xpath("//tr/td[1]/a")[0].attrib["href"]
    if len(re.split("=|&", href)) >= 2:
        oID = re.split("=|&", href)[1]
    else:
        return None
    url = (
        "https://www.hkex.com.hk/eng/sorc/options/stock_options_detail.aspx?action=csv&type=all&oID=%s&ucode=%s"
        % (oID, underlying)
    )
    content = requests.get(url).content.decode("utf-8-sig")
    detail = {}
    for line in content.split("\r\n"):
        arr = line.split(",")
        if len(arr) >= 2:
            key = arr[0]
            val = arr[1].strip()
            detail[key] = val
            if key.find("Last Traded Price") >= 0:
                detail["last_price"] = val
    # print("contract detail.............")
    # print(detail)
    return detail


def history(underlying: str, strike: int, expiry: str, otype: str):
    url = "https://www.hkex.com.hk/eng/sorc/options/stock_options_detail.aspx"
    request_data = {
        "action": "ajax",
        "type": "list",
        "otype": otype,
        "underlying": underlying,
        "expiry": expiry,
        "strike": strike,
        "page": 1,
    }
    option_list_res = requests.post(
        url, data=request_data, headers={
            "referer": "https://www.hkex.com.hk/eng/sorc/options/stock_options_detail.aspx",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
        })
    dom = html.fromstring(option_list_res.text)
    href = dom.xpath("//tr/td[1]/a")[0].attrib["href"]
    oID = re.split("=|&", href)[1]

    # historical data: underlying_price vs option_price
    historical_data = {}
    for data_type in range(1, 4):
        url = (
            "https://www.hkex.com.hk/eng/sorc/options/stock_options_detail.aspx?action=csv&type=%d&oID=%s&ucode=%s"
            % (data_type, oID, underlying)
        )
        content = requests.get(url).content.decode("utf-8-sig")
        first_empty_line_found = False
        header_line_found = False
        for line in content.split("\r\n"):
            if line == "":
                first_empty_line_found = True
                continue
            if not first_empty_line_found:
                continue
            if first_empty_line_found and not header_line_found:
                header_line_found = True
                headers = line.split(",")
                continue

            data_arr = line.split(",")
            trade_date = data_arr[0]
            if trade_date not in historical_data.keys():
                historical_data[trade_date] = {}
            if len(data_arr) != len(headers):
                # print(data_arr)
                break
            for i, attr_name in enumerate(headers):
                historical_data[trade_date][attr_name] = data_arr[i]

    historical_array = []
    for trade_date in historical_data:
        # print(historical_data[trade_date])
        historical_array.append(historical_data[trade_date])

    import pandas as pd

    df = pd.DataFrame(historical_array)
    print(df)
    return df


def search(underlying, strike_range_percent, expiry_before, otype):
    url = "https://www.hkex.com.hk/eng/sorc/options/stock_options_search.aspx"
    request_data = {
        "action": "ajax",
        "type": "search",
        "otype": "ucode",
        "code": underlying,
        "wtype": otype,
        "mdate": "All",
        "moneyness1": str(-1 * strike_range_percent),
        "moneyness2": str(strike_range_percent),
        "premium1": str(0),
        "premium2": str(11),
        "ordering": "ucode_asc",
        "page": 1,
    }
    option_list_res = requests.post(url, data=request_data)
    soup = BeautifulSoup(option_list_res.text, "html.parser")
    print(data)
