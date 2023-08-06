from urllib.parse import urlencode
import json 
import requests

class Client: 
  def init(self, api_key): 
  	self.api_key = api_key
  	self.headers = {
  		'Accept': 'application/json', 
  		'Authorization': self.api_key, 
  		'Content-type': 'application/json'
  	} 

  def list_calendars(filters={}): 
  	url = 'https://datelist.io/api/calendars?' + urlencode(filters.to_a)
    json.loads(requests.get(url, headers: self.headers).text)

  def list_products(filters={}):
  	url = 'https://datelist.io/api/products?' + urlencode(filters.to_a)
    json.loads(requests.get(url, headers: self.headers).text)

  def list_booked_slots(filters={}): 
  	url = 'https://datelist.io/api/booked_slots?' + urlencode(filters.to_a)
    json.loads(requests.get(url, headers: self.headers).text)

  def update_booked_slot(id, data):
  	url = 'https://datelist.io/api/booked_slots/' + str(id)
    json.loads(requests.patch(url, body: data.to_json, headers: self.headers).text)
