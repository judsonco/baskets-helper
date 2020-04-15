'''
Add category relationship
'''
import time
import json
import requests
from requests import HTTPError, ConnectionError


def read_basket_file(filename):
    '''
    Read a sale file for a basket
    (just a straight list of products)
    '''
    out = []
    with open(filename) as basket:
        for line in basket:
            out.append(line.rstrip())
    return out


def make_login_request(username, password):
    '''
    Login as a user
    '''
    data = {'username': username, 'password': password, 'action': 'login'}
    return requests.post('https://judson.biz/admin/login', data)


def make_product_request(products, cookies):
    data = json.dumps([{ 'id': p, 'categories': [{ 'value': 1601 }] } for p in products])
    return requests.put('http://judson.test/admin/products/describe', data=data, cookies=cookies)


if __name__ == '__main__':
    products = read_basket_file('./assets/products.txt')
    print('Logging in')
    judson_cookies = make_login_request('mgeorge', 'Levi88George').cookies
    try:
        print('Sending the request')
        response = make_product_request(products, judson_cookies)
        response.raise_for_status()
    except Exception as e:
        print('Failed to update the products')
        print(e)

