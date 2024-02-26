
import json
import requests
url = "https://gnews.io/api/v4/top-headlines"
params = {
    "category": "general",
    "max" :2,
    "apikey": "35f0b3e6beb8601f4db1d9e6a901e2b4"
}
parsing_data = {}
response = requests.get(url, params=params)

Api_data = response.json()

parsing_data["articles"] = Api_data.get('articles', [])

articles = parsing_data.get('articles',[])

for article in articles:
    # Accessing key-value pairs within each dictionary
    print(article["image"])
    print("-----------")


