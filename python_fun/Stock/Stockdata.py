import requests
from bs4 import BeautifulSoup

# Function to fetch shareholder data
def get_shareholder_data(stock_symbol):
    url = f'https://groww.in/stocks/{stock_symbol}/share-holding'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the Promoter, FI, and DI holdings data
    promoter = soup.find('div', text='Promoter').find_next('div').get_text() if soup.find('div', text='Promoter') else "No Data"
    fi = soup.find('div', text='FI').find_next('div').get_text() if soup.find('div', text='FI') else "No Data"
    di = soup.find('div', text='DI').find_next('div').get_text() if soup.find('div', text='DI') else "No Data"

    return promoter, fi, di

# Test with a stock symbol
stock_symbol = "tatamotors"
promoter, fi, di = get_shareholder_data(stock_symbol)

print(f"Promoter: {promoter}")
print(f"FI: {fi}")
print(f"DI: {di}")
