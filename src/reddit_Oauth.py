import requests
import requests.auth
client_auth = requests.auth.HTTPBasicAuth('PVVlwB0vkQ1jfg', 'VPnxQ7KiuCzOFDgKo-z4x4BZI5U')
post_data = {"grant_type": "password", "username": "bhargav0286", "password": "Bhargavsatya0286#"}
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"}
response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
response = response.json()

print(response)

# headers = {"Authorization": "bearer 664733044707-iTrV8gxWUKeCE_aas45_8WDOrvg", "User-Agent": "reddit bhargav0286"}
# payload = {'q': 'sars-cov-2', 'limit': 100, 'after':'1577836800', 'before': '1601510400', 'subreddit': 'parenting'}
# response = requests.get("https://oauth.reddit.com/subreddits/search", headers=headers, params=payload)
# response = response.json()
# print(response)