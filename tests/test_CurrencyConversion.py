import pytest
from currency_converter import convert_currency

def test_convert_currency_valid():
    assert convert_currency(100, "EUR") == "Amount in USD is equal to 91.00 in Euros"
    assert convert_currency(1, "JPY") == "Amount in USD is equal to 132.50 in Japanese Yens"
    assert convert_currency(50, "AUD") == "Amount in USD is equal to 74.50 in Australian Dollars"
    assert convert_currency(10, "GBP") == "Amount in USD is equal to 7.60 in British Pounds"

def test_convert_currency_invalid_code():
    with pytest.raises(ValueError):
        convert_currency(100, "ABC")

def test_convert_currency_zero_amount():
    assert convert_currency(0, "USD") == "Amount in USD is equal to 0.00 in US Dollars"