import requests
URL = 'http://?:30303/api/prometheuswservice/util'
for i in range(20210201,20210222):
  params = {'accountId':'?','fromDate':i,'toDate':i}
  res = requests.get(URL,params=params)
  print(res.text)