import requests

payload = {'term': 'honeydew'}

r = requests.get(
    "https://itunes.apple.com/search",
    params=payload)

melon_songs = r.json()


