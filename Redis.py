import redis
import requests
import json
import random

r = redis.Redis(host='localhost', port=6379, db=0)


def add_quotes():
    url = 'https://dummyjson.com/quotes'
    response = requests.get(url)
    quotes = json.loads(response.text)['quotes']
    for quote in quotes:
        quote_str = json.dumps(quote)
        r.rpush('quotes', quote_str)
    print('Quotes added to Redis')


def get_random_quote():
    quote_str = r.lindex('quotes', random.randint(0, r.llen('quotes')-1))
    if quote_str:
        quote = json.loads(quote_str)
        print('Random quote:', quote['quote'])
        print('Author:', quote['author'])
    else:
        print('No quotes found in Redis')


while True:
    print('Enter a command:\n1. Add quotes\n2. Get random quote\n3. Quit')
    command = input()
    if command == '1':
        add_quotes()
    elif command == '2':
        get_random_quote()
    elif command == '3':
        break
    else:
        print('Invalid command')
