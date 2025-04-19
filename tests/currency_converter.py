currency_conversion_rates = [
    ('USD', 1.0, 'US Dollars'),
    ('EUR', 0.91, 'Euros'),
    ('GBP', 0.76, 'British Pounds'),
    ('JPY', 132.5, 'Japanese Yens'),
    ('AUD', 1.49, 'Australian Dollars'),
    ('CAD', 1.34, 'Canadian Dollars'),
    ('INR', 82.0, 'Indian Rupees'),
    ('CNY', 6.87, 'Chinese Yuan'),
    ('CHF', 0.91, 'Swiss Francs'),
    ('NZD', 1.61, 'New Zealand Dollars')
]

def convert_currency(USD_amount, to_currency):
    # Search for the currency in the list
    for code, rate, name in currency_conversion_rates:
        if code == to_currency:
            converted_amount = USD_amount * rate
            return f"Amount in USD is equal to {converted_amount:.2f} in {name}"
    
    # If the currency is not found, raise an error
    raise ValueError("Invalid currency code")

# Only run this if the script is executed directly, not when imported
if __name__ == "__main__":
    amount = float(input("Enter the amount in USD: "))
    to_currency = input("Enter the target currency code (USD, EUR, GBP, JPY, AUD, CAD, INR, CNY, CHF, NZD): ").upper()
    try:
        result = convert_currency(amount, to_currency)
        print(result)
    except ValueError as e:
        print(e)