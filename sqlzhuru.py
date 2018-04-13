import requests,json,random
s=requests.session()
data={'loginPassword':'123456','loginId':'18888888887'}
# data=json.dumps(data)
url="http://115.238.64.146:8801/mng/doLogin.json"
end=s.post(url=url,data=data)
print end.text

# url="http://115.238.64.146:8801/mng/merchant/merchantById.json?merchantCode=2342 and user>0"
# end=s.get(url=url)
# print end.text