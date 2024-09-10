import requests

api_key = 'f11523a3-e47e-4cde-942f-04558e8ce101'
# api_key = 'b54bcf4d-1bca-4e8e-9a24-22ff2c3d462c' # sandbox

ENDPOINT="pro-api.coinmarketcap.com" #product
# ENDPOINT="sandbox-api.coinmarketcap.com" #sandbox-api
url = f'https://{ENDPOINT}/v1/cryptocurrency/listings/latest'
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': api_key,
}

params = {
    'start': '1',
    'limit': '10',  # Limit to the top 10 cryptocurrencies
    'convert': 'USD',
}

response = requests.get(url, headers=headers, params=params)
data = response.json()

# Print out the names and prices of the top 10 cryptocurrencies
for crypto in data['data']:
    print(f"{crypto['name']}: ${crypto['quote']['USD']['price']:.2f}")
