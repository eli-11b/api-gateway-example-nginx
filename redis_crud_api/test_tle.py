import requests
import json

BASE_URL = "http://127.0.0.1"


# Sample TLE data
sample_tle_data = {
    "satellite_name": "Hubble Space Telescope",
    "tle1": "1 20580U 90037B   20153.28845139  .00000111  00000-0  00000+0 0  9993",
    "tle2": "2 20580  28.4694 327.5692 0002748 336.7313  23.2995 15.09280881431826"
}

def test_create_or_update_tle():
    print("\nTesting create or update TLE data:")
    url = f"{BASE_URL}/redis/tle/"
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    response = requests.post(url, data=json.dumps(sample_tle_data), headers=headers)
    print("Status code:", response.status_code)
    print("Response:", response.json())

def test_get_tle():
    print("\nTesting get TLE data:")
    url = f"{BASE_URL}/redis/tle/{sample_tle_data['satellite_name']}"
    response = requests.get(url)
    print("Status code:", response.status_code)
    print("Response:", response.json())

def test_delete_tle():
    print("\nTesting delete TLE data:")
    url = f"{BASE_URL}/redis/tle/{sample_tle_data['satellite_name']}"
    response = requests.delete(url)
    print("Status code:", response.status_code)
    print("Response:", response.json())

def test_get_deleted_tle():
    print("\nTesting get deleted TLE data:")
    url = f"{BASE_URL}/redis/tle/{sample_tle_data['satellite_name']}"
    response = requests.get(url)
    print("Status code:", response.status_code)
    print("Response:", response.json())

if __name__ == "__main__":
    # Run the tests in order
    test_create_or_update_tle()
    test_get_tle()
    test_delete_tle()
    test_get_deleted_tle()
