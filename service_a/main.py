# service_a/main.py
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
import requests
import json


app = FastAPI()


@app.get("/users/")
async def read_users():
    return {"message": "List of users as a response from the user service"}

@app.get("/users/docs")
async def show_documentation():
    """
        SUMMARY: Show Swagger documentation
        ARGS: NONE
        RETURNS: redirect to swagger docs        
    """
    return RedirectResponse("http://localhost:8000/docs")



@app.get("/users/redis")
async def read_user():
    url = "http://api-gateway/redis/"
    response = requests.get(url)
    return {"message": response.json()}


@app.post("/users/create_item/")
async def create_key(request: Request):
    try:
        data = await request.json()
        key = data["key"]
        value = data["value"]
        payload = {"key": key, "value":value}
        response = requests.post(url="http://api-gateway/redis/create_item", json=payload)
        if response.status_code == 200:
            return {"response": response.json()}
        else:
            return {"error": "Failed to create item in redis-client service"}
    except Exception as e:
        return {"error": str(e)}
