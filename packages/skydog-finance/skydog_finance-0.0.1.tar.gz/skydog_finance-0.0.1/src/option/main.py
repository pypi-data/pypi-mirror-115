import hkex
import cboe


def option_price(underlying: str, strike: int, expiry: str, otype: "P" | "C"):
    if underlying[-3:].lower() == ".hk":
        hkex.current(underlying, strike, expiry, otype)
    else:
        cboe.get_cboe_option(underlying, strike, expiry, otype)
