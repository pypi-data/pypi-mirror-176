import requests

class Linked :
    def __init__(self) :
        self.url = "http://bigdata-car.kr:5000/APIs/linked-data/"

    def city(self) :
        res = requests.get(self.url + "city-codes")

        return res.text

    def bicycle(self, city, year, key) :
        category = "bicycle"
        res = requests.get(self.url + category + "?city=" + city + "&year=" + year + "&key=" + key)

        return res.text

    def child(self, city, year, key) :
        category = "child"
        res = requests.get(self.url + category + "?city=" + city + "&year=" + year + "&key=" + key)

        return res.text

    def freezing(self, city, year, key) :
        category = "freezing"
        res = requests.get(self.url + category + "?city=" + city + "&year=" + year + "&key=" + key)

        return res.text

    def holiday(self, city, year, key) :
        category = "holiday"
        res = requests.get(self.url + category + "?city=" + city + "&year=" + year + "&key=" + key)

        return res.text

    def jaywalking(self, city, year, key) :
        category = "jaywalking"
        res = requests.get(self.url + category + "?city=" + city + "&year=" + year + "&key=" + key)

        return res.text

    def local(self, city, year, key) :
        category = "local"
        res = requests.get(self.url + category + "?city=" + city + "&year=" + year + "&key=" + key)

        return res.text

    def motorcycle(self, city, year, key) :
        category = "motorcycle"
        res = requests.get(self.url + category + "?city=" + city + "&year=" + year + "&key=" + key)

        return res.text

    def oldman(self, city, year, key) :
        category = "oldman"
        res = requests.get(self.url + category + "?city=" + city + "&year=" + year + "&key=" + key)

        return res.text

    def schoolzone(self, city, year, key) :
        category = "schoolzone"
        res = requests.get(self.url + category + "?city=" + city + "&year=" + year + "&key=" + key)

        return res.text

    def violation(self, city, year, key) :
        category = "violation"
        res = requests.get(self.url + category + "?city=" + city + "&year=" + year + "&key=" + key)

        return res.text

# linked = Linked()
# print(linked.bicycle("11110", "2013099", "uksm5YcI4llc5U2xnKy7bIxbUEbEvAwISBrPnG1udflarvxq59YY%2FXYQ1J3lYHcd"))