from datetime import date
from skydog_option import hkex
from skydog_option import cboe
import logging


def option_price(underlying: str, strike: float, expiry: date, otype: str) -> dict:
    # result = {"underlying": underlying, "strike": strike, "otype": otype}
    logging.debug({"underlying": underlying, "strike": strike, "otype": otype})
    if underlying[-3:].lower() == ".hk":
        return hkex.get_option(underlying, strike, expiry, otype)
    else:
        return cboe.get_option(underlying, strike, expiry, otype)
