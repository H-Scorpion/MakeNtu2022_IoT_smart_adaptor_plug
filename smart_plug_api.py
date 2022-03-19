import requests

api_url = "https://api.thingspeak.com/update?api_key=OR1ZY9CA8P126CKP&field1=0"
data = {"field1":110,"field2":0.023,"field3":110*0.023}

req = requests.get(api_url,data= data)
print(req.text)