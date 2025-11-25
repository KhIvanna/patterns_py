from app.weather.weather_api import WeatherAPI
from app.core.logger import get_logger
from typing import List

logger = get_logger()

class WeatherStation:
    """Observer Subject - notifies observers when weather changes"""
    
    def __init__(self):
        self._observers: List = []
        self._current_weather = None
        self.weather_api = WeatherAPI()
    
    def attach(self, observer):
        """Attach an observer"""
        if observer not in self._observers:
            self._observers.append(observer)
            logger.info(f"Observer {observer.__class__.__name__} attached")
    
    def detach(self, observer):
        """Detach an observer"""
        if observer in self._observers:
            self._observers.remove(observer)
            logger.info(f"Observer {observer.__class__.__name__} detached")
    
    def notify(self):
        """Notify all observers about weather change"""
        logger.info(f"Notifying {len(self._observers)} observers about weather change")
        for observer in self._observers:
            observer.update(self._current_weather)
    
    def fetch_weather(self, city: str):
        """Fetch weather from API and notify if changed"""
        try:
            new_weather = self.weather_api.get_weather(city)
            
            weather_changed = False
            if self._current_weather is None:
                weather_changed = True
                logger.info(f"Initial weather fetch for {city}: {new_weather['condition']}")
            elif self._current_weather.get('condition') != new_weather.get('condition'):
                weather_changed = True
                logger.info(
                    f"Weather changed in {city}: "
                    f"{self._current_weather.get('condition')} -> {new_weather.get('condition')}"
                )
            
            self._current_weather = new_weather
            
            if weather_changed:
                self.notify()
            
            return new_weather
            
        except Exception as e:
            logger.error(f"Error fetching weather: {e}")
            raise
    
    def get_current_weather(self):
        """Get current weather data"""
        return self._current_weather