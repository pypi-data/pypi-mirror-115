from urllib.parse import urlencode
import json 
import requests

class Client: 
  def __init__(self, api_key): 
  	self.api_key = api_key
  	self.headers = {
  		'Accept': 'application/json', 
  		'Authorization': self.api_key, 
  		'Content-type': 'application/json'
  	} 

  def list_calendars(self, filters={}): 
    url = 'https://datelist.io/api/calendars?' + urlencode(filters)
    return requests.get(url, headers= self.headers).json()

  def list_products(self, filters={}):
    url = 'https://datelist.io/api/products?' + urlencode(filters)
    return requests.get(url, headers= self.headers).json()

  def list_booked_slots(self, filters={}): 
    url = 'https://datelist.io/api/booked_slots?' + urlencode(filters)
    return requests.get(url, headers= self.headers).json()

  def update_booked_slot(self, id, data):
    url = 'https://datelist.io/api/booked_slots/' + str(id)
    return requests.patch(url, json= data, headers= self.headers).json()
