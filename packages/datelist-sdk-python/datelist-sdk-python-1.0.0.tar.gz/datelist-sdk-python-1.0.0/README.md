SDK for https://datelist.io in Python

# Usage 

```python 
from datelist.client import Client

client = Client('WGQqyEjfXLtK74K5YuxrHn7v')
calendars = client.list_calendars()
products = client.list_products({ 'calendar_id': 441, 'name': "Table" })
slots = client.list_booked_slots({
  'email': "test@test.com",
  'calendar_id': 441,
  'from': "2021-08-04T04:51:59.945Z",
  'to': "2021-08-30T04:51:59.945Z",
})

print(calendars)
print(products)
print(slots)

print(client.update_booked_slot(slots[0]['id'], {'email': 'test2@test.com'}))
print(client.update_booked_slot(slots[0]['id'], {'email': 'test@test.com'}))
```
