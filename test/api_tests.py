import sys
import requests
import inspect
import json
import random
import string
from random import randint, choice

data = dict()
BASE_URL = 'http://localhost:3000/items'

NUM_ITEMS = int(sys.argv[1])

def random_generator(size=6, chars=string.ascii_uppercase):
	return ''.join(random.choice(chars) for x in range(size))

def test_create_table():
  print('TEST: CREATE TABLE')
  r = requests.post('http://localhost:3000/_create_items_table')
  try:
    response = r.text
    print(response)
    print('\nAttempting to parse JSON...')
    print(json.loads(response), end='\n\n')
  except Exception as e:
    frame = inspect.currentframe()
    print(inspect.getframeinfo(frame).function + ' failed.')
    print(e)


def test_add_item():
  random_text = random_generator(20)

  print('\n\nTEST: ADDING ITEM')
  r = requests.post(BASE_URL, data=json.dumps({
                    "ItemName": random_text}))
  try:
    response = r.text
    print('response is ' + response)
    print('\nAttempting to parse JSON...')
    print(json.loads(response), end='\n\n')
  except Exception as e:
    frame = inspect.currentframe()
    print(inspect.getframeinfo(frame).function + ' failed.')
    print(e)


# def test_get_orders():
  # print('\n\nTEST: GETTING ALL ORDERS')
  # r = requests.get(BASE_URL)
  # try:
    # response = r.text
    # print(response)
    # print('\nAttempting to parse JSON...')
    # global data
    # data = json.loads(response)
    # print(data, end='\n\n')
  # except Exception as e:
    # frame = inspect.currentframe()
    # print(inspect.getframeinfo(frame).function + ' failed.')
    # print(e)


# def test_get_order():
  # print('\n\nTEST: GETTING SPECIFIC ORDERS')
  # if(not data):
    # print('Nothing!')
    # return
  # orders = data['orders']
  # for i in range(len(orders)):
    # r = requests.get(BASE_URL + '/' + orders[i]['orderId'])
    # try:
      # response = r.text
      # print(response)
      # print('\nAttempting to parse JSON...')
      # print(json.loads(response), end='\n\n')
    # except Exception as e:
      # frame = inspect.currentframe()
      # print(inspect.getframeinfo(frame).function + ' failed.')
      # print(e)


# def test_update_order():
  # print('\n\nTEST: UPDATING SPECIFIC ORDERS')
  # if(not data):
    # return
  # orders = data['orders']
  # for i in range(len(orders)):
    # payload = {
      # "customerId": randint(5000, 6000),
      # "preTaxAmount": randint(5000, 6000),
      # "postTaxAmount": randint(5000, 6000),
      # "version": orders[i]['version']
    # }
    # r = requests.post(BASE_URL + '/' + orders[i]['orderId'], data=json.dumps(payload))
    # try:
      # response = r.text
      # print(response, r.status_code)
      # print('\nAttempting to parse JSON...')
      # print(json.loads(response), end='\n\n')
    # except Exception as e:
      # frame = inspect.currentframe()
      # print(inspect.getframeinfo(frame).function + ' failed.')
      # print(e)


# def test_delete_order():
  # print('\n\nTEST: DELETING SPECIFIC ORDERS')
  # if(not data):
    # return
  # orders = data['orders']
  # for i in range(len(orders)):
    # r = requests.delete(BASE_URL + '/' + orders[i]['orderId'])
    # try:
      # response = r.text
      # print(response)
      # print('\nAttempting to parse JSON...')
      # print(json.loads(response), end='\n\n')
    # except Exception as e:
      # frame = inspect.currentframe()
      # print(inspect.getframeinfo(frame).function + ' failed.')
      # print(e)


test_create_table()
  
for i in range(NUM_ITEMS):
  test_add_item()

# test_get_orders()
# test_get_order()
# test_update_order()
# test_delete_order()
# test_get_orders()