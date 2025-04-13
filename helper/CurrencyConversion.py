# Dictionary for currency conversion rates relative to USD
currency_conversion_rates = {
    "USD": 1.0,       # Base currency
    "EUR": 0.91,      # 1 USD = 0.91 EUR
    "GBP": 0.76,      # 1 USD = 0.76 GBP
    "JPY": 132.5,     # 1 USD = 132.5 JPY
    "AUD": 1.49,      # 1 USD = 1.49 AUD
    "CAD": 1.34,      # 1 USD = 1.34 CAD
    "INR": 82.0,      # 1 USD = 82.0 INR
    "CNY": 6.87,      # 1 USD = 6.87 CNY
    "CHF": 0.91,      # 1 USD = 0.91 CHF
    "NZD": 1.61       # 1 USD = 1.61 NZD
}

# Function to convert between currencies
def convert_currency(USD_amount, to_currency):
    if to_currency not in currency_conversion_rates:
        raise ValueError("Invalid currency code")
    
    # Convert the amount to the target currency
    converted_amount = USD_amount * currency_conversion_rates[to_currency]
    
    # Return the formatted statement
    return f"Amount in USD is equal to {converted_amount:.2f} in {to_currency}"

# Get user input
amount = float(input("Enter the amount in USD: "))  # Convert input to a float for numeric calculations
to_currency = input("Enter the target currency code (e.g., EUR, JPY): ").upper()  # Ensure input is uppercase

# Perform the conversion and print the result
try:
    result = convert_currency(amount, to_currency)
    print(result)
except ValueError as e:
    print(e)