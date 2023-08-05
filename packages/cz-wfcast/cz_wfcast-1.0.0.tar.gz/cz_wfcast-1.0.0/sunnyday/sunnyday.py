import requests

# url = "http://api.openweathermap.org/data/2.5/forecast?q=Madrid&appid=01a8c19d7a22e4b247188569dad18833&units=imperial"
# r = requests.get(url)
# print(r.json())

class Weather:
    
    def __init__(self, apikey, city=None, lat=None, lon=None):
        if city:
            url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={apikey}&units=imperial"
            r = requests.get(url)
            self.data = r.json()
        elif lat and lon:
            url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={apikey}&units=imperial"
            r = requests.get(url)
            self.data = r.json()
        else:
            raise TypeError("Provide either a city name or lat and lon arguments")
        
        if self.data["cod"] != "200":
            raise ValueError(self.data["message"])
    
    def next_12h(self):
        return self.data['list'][:4]
    
    def next_12h_simplified(self):
        simple_data = []
        for dicty in self.data['list'][:4]:
            simple_data.append((dicty['dt_txt'], dicty['main']['temp'], dicty['weather'][0]['description']))
        return simple_data
        #return (self.data['list'][0]['dt_txt'], self.data['list'][0]['main']['temp'], self.data['list'][0]['weather'][0]['description'])
