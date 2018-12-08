import requests
import json
class Weather:
    api_url = 'https://api.openweathermap.org/data/2.5/weather'
    api_key = "32b9477a3c48ef090c4b145b091324d9"
    r = None
    results = []
    def __init__(self, locations):
        self.results = []
        for location in locations:
            print("Making request for ", location)
            if location["LocationCode"] == 1:
                lat = location["Latitude"]
                long = location["Longitude"]
                self.r = requests.get(self.api_url, params={'lat': lat, 'lon': long, 'appid': self.api_key, 'units': 'imperial'})	
            elif location["LocationCode"] == 0:
                zip = location["ZipCode"]
                self.r = requests.get(self.api_url, params={'zip': zip + ',us', appid: self.api_key, 'units': 'imperial'})
            elif location["LocationCode"] == 2:
                city = locations["City"]
                country = location["Country"]
                self.r = requests.get(self.api_url, params={'q': city +',' + country, appid: self.api_key, 'units': 'imperial'})
            print(self.r.text)
            r_j = json.loads(self.r.text)
            self.results.append(r_j)


