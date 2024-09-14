# redis/main.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
import redis
from models import RequestBody, Key, JsonData, ListNameRequest, TLEData
import json

app = FastAPI()
client = redis.Redis(host='redis', port=6379, db=0)


@app.get("/redis/")
async def test_connection():
    """
        SUMMARY: Ping the redis server to make sure connection is okay
        ARGS: NONE
        RETURNS: (STATUS) connection success or not
    """
    try:
        # Attempt to ping the Redis server
        client.ping()
        return {"status": "success", "message": "Connected to Redis"}
    except redis.ConnectionError as e:
        return {"status": "error", "message": str(e)}

@app.get("/redis/docs")
async def show_documentation():
    """
        SUMMARY: Show Swagger documentation
        ARGS: NONE
        RETURNS: redirect to swagger docs        
    """
    return RedirectResponse("http://localhost:8004/docs")


@app.post("/redis/create_item/")
async def create_key(body: RequestBody):
    """
        SUMMARY: Creates an item in redis server
        ARGS: (body:RequestBody) json payload
        RETURNS: (response:json) the json response after creating item or failing to do so. 
    """
    try:
        response = client.set(body.key, body.value)
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}



@app.post("/redis/get_item/")
async def get_data(key: Key):
    """
        SUMMARY: Retrieves an item in redis server
        ARGS: (key:Key) json payload
        RETURNS: (response:json) the json data in response form after retrieving item or failing to do so. 
    """
    try:
        response = client.get(key.key)
        print(response)
        if response is None:
            return {"error": "Key not found"}
        return {"data": response.decode('utf-8')}
    except Exception as e:
        return {"error": e}


@app.post("/redis/create_list")
async def create_list(json_data: JsonData):
    """
        SUMMARY: Create a json data to store in a list on redis
        ARGS: (json_data: JsonData) json payload
        RETURNS: (response:json) the json data in response form after creating the list in redis or failing to do so. 
    """
    try:
        payload = json.dumps(json_data.payload)
        response = client.rpush(json_data.list_name, payload)
        return {"response":f"created list {json_data.list_name}"}
    except Exception as e:
        return {"error": str(e)}


@app.post("/redis/read_list")
async def read_list(request: ListNameRequest):
        """
        SUMMARY: Read json data from list stored on redis
        ARGS: (request:ListNameRequest) The listname for the request
        RETURNS: json data from a list in redis or response from failing to do so. 
    """
    try:
        response = client.lrange(request.listname, 0, -1)
        # Convert byte values to UTF-8 strings
        results = [json.loads(item.decode('utf-8')) for item in response]
        return {"results": results}
    except Exception as e:
        return {"error": str(e)}


#### TLE DATA ####

"""
sample_tle_data = {
    "satellite_name": "Hubble Space Telescope",
    "tle1": "1 20580U 90037B   20153.28845139  .00000111  00000-0  00000+0 0  9993",
    "tle2": "2 20580  28.4694 327.5692 0002748 336.7313  23.2995 15.09280881431826"
}


## In a curl POST request:

curl -X POST "http://127.0.0.1:8008/tle/" -H "Content-Type: application/json" -d '{
    "satellite_name": "Hubble Space Telescope",
    "tle1": "1 20580U 90037B   20153.28845139  .00000111  00000-0  00000+0 0  9993",
    "tle2": "2 20580  28.4694 327.5692 0002748 336.7313  23.2995 15.09280881431826"
}'


"""

# Function to store TLE data in Redis
def store_tle_data(redis_client: redis.Redis, tle_data: TLEData):
    """
        SUMMARY: Store TLE Data in Redis
        ARGS: (redis_client) The client connecting to the redis server. 
        ARGS: (tle_data:TLEDATA) tle data in as a json payload 
        RETURNS: NONE        
    """
    redis_key = f"tle:{tle_data.satellite_name}"
    
    # Store TLE data as a hash
    redis_client.hset(redis_key, mapping=tle_data.dict())
    
    print(f"TLE data for {tle_data.satellite_name} stored in Redis under key {redis_key}")

# Function to retrieve TLE data from Redis
def retrieve_tle_data(redis_client: redis.Redis, satellite_name: str) -> TLEData:
    """
        SUMMARY: Retreive TLE Data in Redis
        ARGS: (redis_client) The client connecting to the redis server. 
        ARGS: (satellite_name:str) satellite name 
        RETURNS: NONE        
    """
    redis_key = f"tle:{satellite_name}"
    stored_data = redis_client.hgetall(redis_key)
    
    if not stored_data:
        raise HTTPException(status_code=404, detail=f"No TLE data found for satellite {satellite_name}")
    
    # Convert byte strings to regular strings
    stored_data = {k.decode('utf-8'): v.decode('utf-8') for k, v in stored_data.items()}
    
    return TLEData(**stored_data)


# Create or update TLE data
@app.post("/redis/tle/", response_model=TLEData)
async def create_or_update_tle(tle_data: TLEData):
    store_tle_data(client, tle_data)
    return tle_data


# Get TLE data by satellite name
@app.get("/redis/tle/{satellite_name}", response_model=TLEData)
async def get_tle(satellite_name: str):
    return retrieve_tle_data(client, satellite_name)


# Delete TLE data by satellite name
@app.delete("/redis/tle/{satellite_name}")
async def delete_tle(satellite_name: str):
    redis_key = f"tle:{satellite_name}"
    result = client.delete(redis_key)
    
    if result == 0:
        raise HTTPException(status_code=404, detail=f"No TLE data found for satellite {satellite_name}")
    
    return {"message": f"TLE data for satellite {satellite_name} deleted successfully"}
