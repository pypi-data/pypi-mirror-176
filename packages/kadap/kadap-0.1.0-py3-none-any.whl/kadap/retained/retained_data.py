import requests

class Retained :
    def __init__(self) :
        self.url = "http://bigdata-car.kr:5000/APIs/retained-data/retained"

    def getData(self, id) :
        params = {"id": id}
        res = requests.get(url=self.url, params=params)

        return res.text

retained = Retained()
print(retained.getData("maintenance"))