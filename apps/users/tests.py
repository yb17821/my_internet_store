from django.test import TestCase
import re
# Create your tests here.
import requests
import json
url = 'http://127.0.0.1:8000/login/'
url2 = 'http://127.0.0.1:8000/address/'
response = requests.get(url)
response.encoding = 'utf-8'
csrftoken = re.compile('<input type="hidden" name="csrfmiddlewaretoken" value="(.+?)">').findall(response.text)
print(response.text)
exit()
data = {
    'username':'18895326641',
    'password':'yb1122yb',
    'code':'6666',
    'csrfmiddlewaretoken': csrftoken
}
res = requests.post(url,data=data)
res.encoding = 'utf-8'
print(res.text)
exit()
token = json.loads(res.text)['token']
headers={
        'Authorization':'JWT %s' % token,
}
print(token)
res = requests.get(url2,headers = headers)
res.encoding = 'utf-8'
print(res.text)

