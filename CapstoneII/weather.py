import requests

class Weather:
	api_url = 'https://api.openweathermap.org/data/2.5/weather'
	api_key = "32b9477a3c48ef090c4b145b091324d9"
	r = None
	def __init__(self, locations):
		print("Making request for ", locations)
		if locations["LocationCode"] == 1:
			lat = locations["Latitude"]
			long = locations["Longitude"]
			self.r = requests.get(self.api_url, params={'lat': lat, 'lon': long, 'appid': self.api_key})	
		elif locations["LocationCode"] == 0:
			zip = locations["ZipCode"]
			self.r = requests.get(self.api_url, params={'zip': zip + ',us', appid: self.api_key})
		elif locations["LocationCode"] == 2:
			city = locations["City"]
			country = locations["Country"]
			self.r = requests.get(self.api_url, params={'q': city +',' + country, appid: self.api_key})
	
	def get_results(self):
		return self.r.text