import os
import requests
from dotenv import load_dotenv

# Load key from .env file
load_dotenv()

api_key = os.getenv("ONET_API_KEY")
if not api_key:
    print("❌ Error: ONET_API_KEY not found in .env file.")
    exit(1)

headers = {
    "X-API-Key": api_key,
    "Accept": "application/json"
}

url = "https://api-v2.onetcenter.org/about/"
print(f"Pinging O*NET API at {url}...\n")

try:
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print("✅ Handshake Successful!")
        print(f"O*NET API Version: {data.get('api_version')}")
        print(f"Database: {data.get('database', {}).get('name')}")
        print(f"Taxonomy: {data.get('taxonomy', {}).get('name')}")
    else:
        print(f"❌ Handshake Failed! HTTP Status Code: {response.status_code}")
        print(f"Error Message: {response.text}")
except Exception as e:
    print(f"❌ Connection Error: {e}")
