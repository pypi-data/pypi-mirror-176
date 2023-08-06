import requests

class VIN :
    def __init__(self) :
        self.url = "http://bigdata-car.kr:5000/APIs/vin-decoder?VIN="
    
    def decoded(self, code) :
        res = requests.get(self.url + code)

        return res.text

# vin = VIN()
# print(vin.decoded("KMHEM44CPLU123456"))