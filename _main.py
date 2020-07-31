import os
import requests
import logging
import argparse
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.DEBUG)

BITLY_TOKEN = os.getenv('BITLY_TOKEN')


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument ('link', help='Введите ссылку') 
    return parser

def shorten_link(token, url):
    headers = {'Authorization': f'Bearer {token}'}
    payload = {'long_url': url}
    shorten = 'https://api-ssl.bitly.com/v4/shorten'
    response = requests.post(shorten,
                          headers=headers,
                          json=payload)
    response.raise_for_status()
    return response.json()['link']

def count_clicks(token, symbols):
    headers = {'Authorization': f'Bearer {token}'}
    params = {'unit': 'month', 'units ': -1}
    summary = f'https://api-ssl.bitly.com/v4/bitlinks/bit.ly/{symbols}/clicks/summary'
    response = requests.get(summary,
                          headers=headers,
                          params=params)
    return response.json()['total_clicks']

def main():
    parser = createParser()
    link = parser.parse_args()
    
    if 'bit.ly' in link.name:
        symbols = url.split('/')[-1]
        try:
          number = count_clicks(BITLY_TOKEN, symbols)
        except requests.exceptions.HTTPError as e:
          print('HTTP response status:', e.response.status_code)
        print(f'Кол-во кликов ', number)
    else:
        try:
          bitlink = shorten_link(BITLY_TOKEN, url)
        except requests.exceptions.HTTPError as e:
          print('HTTP response status:', e.response.status_code)
        print('Битлинк', bitlink)

if __name__ == '__main__':
    main()
