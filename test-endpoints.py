import requests
import json


# template
# url = "http://localhost:8080"
# data = {'sender': 'Alice', 'receiver': 'Bob', 'message': 'We did it!'}
# headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
# r = requests.post(url/{endpoint}, data=json.dumps(data), headers=headers)

print()
print("testing example endpoint /users")
print("should return: {'message': 'List of users as a response from the user service'}")
response = requests.get("http://127.0.0.1/users")
print(response.json())


print()
print("testing example endpoint /products")
print("should return: {'message': 'List of products as a response from the products service'}")
response = requests.get("http://127.0.0.1/products")
print(response.json())



# test creating key in redis
print("")
print("testing creating key redis: should return {'response':'true'}")
url = "http://127.0.0.1/redis/create_item"
data = {"key": "eli-test", "value": "eli-test-value"}
print(data)
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
response = requests.post(url, data=json.dumps(data), headers=headers)
print(response.json())


# test reading key in redis
print("")
print("testing reading from redis: should return {'data':'eli-test-value'}")
url = "http://127.0.0.1/redis/get_item"
data = {"key": "eli-test"}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
response = requests.post(url, data=json.dumps(data), headers=headers)
print(response.json())

#test writing json data to redis
print("")
print("testing reading from redis: should return {'response':'created list'}")
url = "http://127.0.0.1/redis/create_list"
data = {"list_name": "json_list5", "payload": {"key1": "value1", "key2": "value2"}}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
response = requests.post(url, data=json.dumps(data), headers=headers)
print(response.json())


#test reading json data from redis
print("")
print("testing reading from redis: should return {'results':['key1':'value1', 'key2':'value2'] etc..")
url = "http://127.0.0.1/redis/read_list"
data = {"listname": "json_list5"}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
response = requests.post(url, data=json.dumps(data), headers=headers)
print(response.json())