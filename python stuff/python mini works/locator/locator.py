import requests
res=requests.get('https://ipinfo.io/')
data=res.json()
print(data)