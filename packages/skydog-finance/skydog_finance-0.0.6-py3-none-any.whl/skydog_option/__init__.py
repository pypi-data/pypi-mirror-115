from skydog_option import hkex
from skydog_option import cboe


def option_price(underlying: str, strike: int, expiry: str, otype: str):
    result = {"underlying": underlying, "strike": strike, "otype": otype}
    if underlying[-3:].lower() == ".hk":
        return hkex.get_option(underlying, strike, expiry, otype)
    else:
        return cboe.get_option(underlying, strike, expiry, otype)
