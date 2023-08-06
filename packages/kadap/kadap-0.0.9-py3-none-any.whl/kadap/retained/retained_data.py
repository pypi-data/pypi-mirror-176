import requests

class Retained :
    def __init__(self) :
        self.url = "http://bigdata-car.iptime.org:3455/APIs/retained-data/retained?ID="

    def getData(self, id) :
        res = requests.get(self.url + id)

        return res.text

# retained = Retained()
# print(retained.getData("maintenance"))