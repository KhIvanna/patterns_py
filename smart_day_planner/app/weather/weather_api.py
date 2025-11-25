import requests
from app.core.config import API_KEY, WEATHER_API_URL
from app.core.logger import get_logger

logger = get_logger()

class WeatherAPI:
    """Integration with OpenWeatherMap API"""
    
    def __init__(self):
        self.api_key = API_KEY
        self.base_url = WEATHER_API_URL
    
    def get_weather(self, city: str) -> dict:
        """
        Fetch weather data from OpenWeatherMap API
        Returns: dict with weather info
        """
        try:
            url = f"{self.base_url}?q={city}&appid={self.api_key}&units=metric"
            
            logger.info(f"Fetching weather for {city}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            weather_info = {
                "city": city,
                "condition": self._map_weather_condition(data['weather'][0]['main']),
                "description": data['weather'][0]['description'],
                "temperature": round(data['main']['temp']),
                "feels_like": round(data['main']['feels_like']),
                "humidity": data['main']['humidity'],
                "timestamp": data['dt']
            }
            
            logger.info(f"Weather fetched: {city} - {weather_info['condition']}, {weather_info['temperature']}°C")
            return weather_info
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise Exception(f"Failed to fetch weather data: {e}")
        except KeyError as e:
            logger.error(f"Unexpected API response format: {e}")
            raise Exception(f"Invalid weather data received: {e}")
    
    def _map_weather_condition(self, condition: str) -> str:
        """
        Map OpenWeatherMap conditions to our strategy types
        Possible values: Sunny, Rainy, Cloudy, Snowy
        """
        condition = condition.lower()
        
        if condition in ['clear']:
            return 'Sunny'
        elif condition in ['rain', 'drizzle', 'thunderstorm']:
            return 'Rainy'
        elif condition in ['clouds', 'mist', 'fog', 'haze']:
            return 'Cloudy'
        elif condition in ['snow', 'sleet']:
            return 'Snowy'
        else:
            return 'Cloudy'  