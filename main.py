import os
import requests
import logging
import argparse
from dotenv import load_dotenv


logging.basicConfig(level=logging.DEBUG)


def parse_argument(): 
  parser = argparse.ArgumentParser()
  parser.add_argument ('name', help='Введите ссылку') 
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
  load_dotenv()

  parser = parse_argument()
  url = parser.parse_args()

  bitly_token = os.getenv('BITLY_TOKEN')
  
  if 'bit.ly' in url.name:
      symbols = url.name.split('/')[-1]
      try:
        number = count_clicks(bitly_token, symbols)
      except requests.exceptions.HTTPError as e:
        print('HTTP response status:', e.response.status_code)
      print(f'Кол-во кликов ', number)
  else:
      try:
        bitlink = shorten_link(bitly_token, url.name)
      except requests.exceptions.HTTPError as e:
        print('HTTP response status:', e.response.status_code)
      print('Битлинк', bitlink)

if __name__ == '__main__':
  main()
