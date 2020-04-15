'''
Makes a request to the Judson API
'''
import time
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


def request_to_add_basket_item(basket_id, product, quantity, cookies):
    '''
    Make a request to the Judson API to add a basket
    '''
    data = {'products_model': product, 'quantity': quantity}
    return requests.post(
        'https://judson.biz/admin/baskets/%s/items' % basket_id,
        data=data,
        cookies=cookies
    )


def request_to_create_basket(basket_type, num, cookies):
    '''
    Create a new basket through the admin pages
    '''
    data = {
        'type': basket_type,
        'name': 'Premier Sale - %d' % num
    }
    return requests.post('https://judson.biz/admin/baskets', data=data, cookies=cookies, headers={
        'accept': 'application/json'
    })


def make_login_request(username, password):
    '''
    Login as a user
    '''
    data = {'username': username, 'password': password, 'action': 'login'}
    return requests.post('https://judson.biz/admin/login', data)


# if __name__ == '__main__':
#     response = make_login_request('mgeorge', 'Levi88George')
#     judson_cookies = {}
#     judson_cookies['judson-admin'] = response.cookies['judson-admin']
#     current_basket = request_to_create_basket(2, 1, 9999, judson_cookies)
#     print(current_basket.json())


if __name__ == '__main__':
    username = ""
    password = ""
    current_basket = None
    current_basket_index = 0
    response = make_login_request(username, password)
    judson_cookies = {}
    judson_cookies['judson-admin'] = response.cookies['judson-admin']
    products = read_basket_file('./assets/products.txt')
    products_to_retry = products[0:10]
    for (i, product) in enumerate(products, start=0):
        if not current_basket:
            print('Creating basket %d' % i)
            current_basket_index += 1
            try:
                current_basket = request_to_create_basket(2, current_basket_index, judson_cookies).json()
            except:
                print('Failed to create a basket... aborting')
                products_to_retry.append(product)
                break
        print('Requesting to add %s' % product)
        try:
            add_response = request_to_add_basket_item(current_basket['id'], product, 1, judson_cookies)
            add_response.raise_for_status()
        except ConnectionError:
            print('Failed to add a basket item due to timeout... aborting')
            products_to_retry.append(product)
            break
        except HTTPError:
            print('Failed to add a basket item due to HTTP status... aborting')
            products_to_retry.append(product)
        if int(i) != 0 and int(i) % 350 == 0:
            current_basket = None

    if products_to_retry:
        print('Failed to add some products')
        out = ''
        for product in products_to_retry:
            out += '%s\n' % product
        with open('./assets/%s-failed.txt' % time.time(), 'w') as failed_file:
            failed_file.write(out)
