"""
All tests for Smart Day Planner
Run with: pytest tests/all_tests.py -v
"""
import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.weather.weather_station import WeatherStation
from app.weather.weather_api import WeatherAPI
from app.planner.day_planner import DayPlanner
from app.planner.strategies.sunny import SunnyWeatherStrategy
from app.planner.strategies.rainy import RainyWeatherStrategy
from app.planner.strategies.cloudy import CloudyWeatherStrategy
from app.planner.strategies.snowy import SnowyWeatherStrategy

@pytest.fixture
def mock_db():
    """Mock database for testing (no real MongoDB needed)"""
    mock = MagicMock()
    
    mock.get_user_preferences.return_value = {
        "user_id": "test_user",
        "location": "Lviv",
        "preferences": {
            "preferred_types": ["outdoor", "learning"],
            "avoid_types": [],
            "working_hours": {"start": 9, "end": 17},
            "weekend_mode": "relax"
        }
    }
    
    mock._plans = []
    
    def save_plan_mock(plan):
        mock._plans.append(plan)
        return True
    
    def get_current_plan_mock():
        return mock._plans[-1] if mock._plans else None
    
    def get_plans_history_mock(limit=10):
        return mock._plans[-limit:] if mock._plans else []
    
    mock.save_plan = save_plan_mock
    mock.get_current_plan = get_current_plan_mock
    mock.get_plans_history = get_plans_history_mock
    mock.update_user_preferences = MagicMock(return_value=True)
    
    return mock


@pytest.fixture
def weather_station():
    """Weather station instance"""
    return WeatherStation()


@pytest.fixture
def day_planner(mock_db, weather_station):
    """Day planner instance with mocked dependencies"""
    planner = DayPlanner(mock_db, weather_station)
    weather_station.attach(planner)
    return planner


@pytest.fixture
def sample_weather_data():
    """Sample weather data for testing"""
    return {
        "city": "Lviv",
        "condition": "Sunny",
        "description": "clear sky",
        "temperature": 25,
        "feels_like": 23,
        "humidity": 60,
        "timestamp": 1700000000
    }


@pytest.fixture
def sample_user_preferences():
    """Sample user preferences"""
    return {
        "user_id": "test_user_123",
        "location": "Lviv",
        "preferences": {
            "preferred_types": ["outdoor", "learning"],
            "avoid_types": ["sport"],
            "working_hours": {"start": 9, "end": 17},
            "weekend_mode": "Always relax on Sundays"
        }
    }

class TestWeatherStation:
    """Test WeatherStation (Observer Subject)"""
    
    def test_01_attach_observer(self, weather_station):
        """Test 1: Attaching an observer to WeatherStation"""
        observer = Mock()
        weather_station.attach(observer)
        assert observer in weather_station._observers
        print(" Test 1: Observer attached successfully")
    
    def test_02_detach_observer(self, weather_station):
        """Test 2: Detaching an observer from WeatherStation"""
        observer = Mock()
        weather_station.attach(observer)
        weather_station.detach(observer)
        assert observer not in weather_station._observers
        print(" Test 2: Observer detached successfully")
    
    def test_03_notify_observers(self, weather_station):
        """Test 3: Notifying all observers when weather changes"""
        observer1 = Mock()
        observer2 = Mock()
        
        weather_station.attach(observer1)
        weather_station.attach(observer2)
        
        weather_station._current_weather = {"condition": "Sunny"}
        weather_station.notify()
        
        observer1.update.assert_called_once()
        observer2.update.assert_called_once()
        print(" Test 3: All observers notified successfully")
    
    @patch('app.weather.weather_api.WeatherAPI.get_weather')
    def test_04_fetch_weather_success(self, mock_get_weather, weather_station):
        """Test 4: Successful weather fetch from API"""
        mock_weather = {
            "city": "Lviv",
            "condition": "Sunny",
            "temperature": 25,
            "description": "clear sky",
            "feels_like": 23,
            "humidity": 60,
            "timestamp": 1700000000
        }
        mock_get_weather.return_value = mock_weather
        
        result = weather_station.fetch_weather("Lviv")
        
        assert result == mock_weather
        assert weather_station._current_weather == mock_weather
        print(" Test 4: Weather fetched successfully")
    
    @patch('app.weather.weather_api.WeatherAPI.get_weather')
    def test_05_weather_change_triggers_notify(self, mock_get_weather, weather_station):
        """Test 5: Weather change triggers observer notification"""
        observer = Mock()
        weather_station.attach(observer)
        
        mock_get_weather.return_value = {
            "condition": "Sunny", 
            "city": "Lviv", 
            "temperature": 25,
            "description": "clear",
            "feels_like": 23,
            "humidity": 60,
            "timestamp": 1700000000
        }
        weather_station.fetch_weather("Lviv")
        
        mock_get_weather.return_value = {
            "condition": "Rainy", 
            "city": "Lviv", 
            "temperature": 15,
            "description": "rain",
            "feels_like": 13,
            "humidity": 80,
            "timestamp": 1700003600
        }
        weather_station.fetch_weather("Lviv")
        
        assert observer.update.call_count == 2
        print(" Test 5: Weather change triggered notification")

class TestWeatherStrategies:
    """Test Strategy Pattern implementation"""
    
    def test_06_sunny_strategy_returns_outdoor_activities(self):
        """Test 6: Sunny strategy returns outdoor activities"""
        strategy = SunnyWeatherStrategy()
        preferences = {
            "preferred_types": ["outdoor"],
            "avoid_types": [],
            "working_hours": {"start": 9, "end": 17},
            "weekend_mode": "relax"
        }
        
        activities = strategy.get_activities(preferences)
        
        assert len(activities) > 0
        assert any(act['name'] == 'Hiking' for act in activities)
        print(" Test 6: Sunny strategy returns outdoor activities")
    
    def test_07_rainy_strategy_returns_indoor_activities(self):
        """Test 7: Rainy strategy returns indoor activities"""
        strategy = RainyWeatherStrategy()
        preferences = {
            "preferred_types": ["indoor", "productive"],
            "avoid_types": [],
            "working_hours": {"start": 9, "end": 17},
            "weekend_mode": "relax"
        }
        
        activities = strategy.get_activities(preferences)
        
        assert len(activities) > 0
        assert any(act['name'] == 'HouseWork' for act in activities)
        print(" Test 7: Rainy strategy returns indoor activities")
    
    def test_08_cloudy_strategy_returns_mixed_activities(self):
        """Test 8: Cloudy strategy returns mixed activities"""
        strategy = CloudyWeatherStrategy()
        preferences = {
            "preferred_types": ["productive"],
            "avoid_types": [],
            "working_hours": {"start": 9, "end": 17},
            "weekend_mode": "relax"
        }
        
        activities = strategy.get_activities(preferences)
        
        assert len(activities) > 0
        assert any(act['name'] == 'Studying' for act in activities)
        print(" Test 8: Cloudy strategy returns mixed activities")
    
    def test_09_snowy_strategy_returns_winter_activities(self):
        """Test 9: Snowy strategy returns winter activities"""
        strategy = SnowyWeatherStrategy()
        preferences = {
            "preferred_types": ["indoor"],
            "avoid_types": [],
            "working_hours": {"start": 9, "end": 17},
            "weekend_mode": "relax"
        }
        
        activities = strategy.get_activities(preferences)
        
        assert len(activities) > 0
        assert any(act['name'] in ['HouseWork', 'Studying'] for act in activities)
        print(" Test 9: Snowy strategy returns winter activities")
    
    def test_10_strategy_filters_by_avoid_types(self):
        """Test 10: Strategies filter out avoided activity types"""
        strategy = SunnyWeatherStrategy()
        preferences = {
            "preferred_types": [],
            "avoid_types": ["outdoor"], 
            "working_hours": {"start": 9, "end": 17},
            "weekend_mode": "relax"
        }
        
        activities = strategy.get_activities(preferences)
        
        assert not any(act['type'] == 'outdoor' for act in activities)
        print(" Test 10: Strategy correctly filters avoided types")


class TestDayPlanner:
    """Test DayPlanner (Context + Observer)"""
    
    def test_11_day_planner_as_observer(self, sample_weather_data):
        """Test 11: DayPlanner acts as an observer and updates on weather change"""
        
        mock_db = MagicMock()
        mock_db.get_user_preferences.return_value = {
            "user_id": "test_user_123",
            "location": "Lviv",
            "preferences": {
                "preferred_types": ["outdoor", "learning"],
                "avoid_types": ["sport"],
                "working_hours": {"start": 9, "end": 17},
                "weekend_mode": "Always relax on Sundays"
            }
        }
        
        plans_storage = []
        
        def save_plan(plan):
            plans_storage.append(plan)
            return True
        
        def get_current():
            return plans_storage[-1] if plans_storage else None
        
        mock_db.save_plan = save_plan
        mock_db.get_current_plan = get_current
        
        weather_station = WeatherStation()
        day_planner = DayPlanner(mock_db, weather_station)
        weather_station.attach(day_planner)
        
        day_planner.update(sample_weather_data)

        assert len(plans_storage) > 0
        plan = get_current()
        assert plan is not None
        assert plan['location'] == sample_weather_data['city']
        print(" Test 11: DayPlanner correctly acts as observer")
    
    def test_12_strategy_selection_based_on_weather(self):
        """Test 12: Correct strategy is selected based on weather condition"""

        mock_db = MagicMock()
        mock_db.get_user_preferences.return_value = {
            "user_id": "test_user",
            "location": "Lviv",
            "preferences": {
                "preferred_types": ["outdoor", "indoor", "productive", "learning"],
                "avoid_types": [],
                "working_hours": {"start": 9, "end": 17},
                "weekend_mode": "relax"
            }
        }
        
        saved_plans = []
        
        def save_plan_mock(plan):
            saved_plans.append(plan)
            return True
        
        mock_db.save_plan = save_plan_mock
        mock_db.get_current_plan = lambda: saved_plans[-1] if saved_plans else None
        
        weather_station = WeatherStation()
        day_planner = DayPlanner(mock_db, weather_station)
        
        weather_tests = [
            ("Sunny", ["Hiking", "Sport", "Date"]),      
            ("Rainy", ["HouseWork", "Studying", "Date"]), 
            ("Cloudy", ["Studying", "Sport", "Date"]),    
            ("Snowy", ["HouseWork", "Studying", "Date"])   
        ]
        
        for condition, expected_activities in weather_tests:
            weather = {
                "condition": condition,
                "city": "Lviv",
                "temperature": 20,
                "description": "test"
            }
            day_planner.update(weather)
            
            plan = mock_db.get_current_plan()
            assert plan is not None, f"Plan should not be None for {condition}"
            assert plan['weather']['condition'] == condition, f"Weather condition mismatch for {condition}"
            
            activity_names = [act['name'] for act in plan['activities']]
            has_expected = any(expected in activity_names for expected in expected_activities)
            assert has_expected, f"Expected one of {expected_activities} but got {activity_names} for {condition}"
        
        print(" Test 12: Correct strategy selected for each weather condition")

class TestDatabaseOperations:
    """Test database operations (fully mocked)"""
    
    def test_13_database_save_and_retrieve_operations(self, mock_db):
        """Test 13: Database save and retrieve operations work correctly"""
       
        user_prefs = {
            "user_id": "test_user_456",
            "location": "Kyiv",
            "preferences": {
                "preferred_types": ["learning"],
                "avoid_types": ["sport"],
                "working_hours": {"start": 10, "end": 18},
                "weekend_mode": "relax"
            }
        }
        
        mock_db.update_user_preferences("test_user_456", user_prefs)
        assert mock_db.update_user_preferences.called
        
       
        plan = {
            "date": "2025-11-22",
            "time_generated": "2025-11-22 10:00:00",
            "location": "Kyiv",
            "weather": {"condition": "Sunny", "temperature": 25, "description": "clear"},
            "activities": [
                {"name": "Hiking", "type": "outdoor", "priority": 5}
            ],
            "user_id": "test_user_456"
        }
        
        result = mock_db.save_plan(plan)
        assert result == True
        
        
        retrieved_plan = mock_db.get_current_plan()
        assert retrieved_plan is not None
        assert retrieved_plan['location'] == "Kyiv"
        
       
        history = mock_db.get_plans_history(limit=1)
        assert len(history) >= 1
        
        print(" Test 13: Database operations working correctly")

class TestWeatherAPI:
    """Test OpenWeatherMap API integration"""
    
    @patch('requests.get')
    def test_14_weather_api_condition_mapping(self, mock_get):
        """Test 14: API weather conditions are mapped correctly to strategies"""
        api = WeatherAPI()
        
        test_cases = [
            ('Clear', 'Sunny'),
            ('Rain', 'Rainy'),
            ('Clouds', 'Cloudy'),
            ('Snow', 'Snowy'),
        ]
        
        for api_condition, expected in test_cases:
            mock_response = Mock()
            mock_response.json.return_value = {
                'weather': [{'main': api_condition, 'description': 'test'}],
                'main': {'temp': 20, 'feels_like': 18, 'humidity': 50},
                'dt': 1700000000
            }
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response
            
            result = api.get_weather("Test")
            assert result['condition'] == expected
        
        print(" Test 14: Weather API conditions mapped correctly")

class TestIntegration:
    """Integration tests for the entire system"""
    
    @patch('app.weather.weather_api.WeatherAPI.get_weather')
    def test_15_full_observer_and_strategy_integration(self, mock_get_weather):
        """Test 15: Complete flow - Weather change → Observer notification → Strategy selection → Plan generation"""
        
        mock_db = MagicMock()
        saved_plans = []
        
        def save_plan_mock(plan):
            saved_plans.append(plan)
            return True
        
        def get_current_plan_mock():
            return saved_plans[-1] if saved_plans else None
        
        mock_db.save_plan = save_plan_mock
        mock_db.get_current_plan = get_current_plan_mock
        mock_db.get_user_preferences.return_value = {
            "user_id": "test_user_789",
            "location": "Lviv",
            "preferences": {
                "preferred_types": ["outdoor", "indoor"],
                "avoid_types": [],
                "working_hours": {"start": 9, "end": 17},
                "weekend_mode": "relax"
            }
        }
        
        weather_station = WeatherStation()
        day_planner = DayPlanner(mock_db, weather_station)
        weather_station.attach(day_planner)
        
        mock_get_weather.return_value = {
            "city": "Lviv",
            "condition": "Sunny",
            "temperature": 25,
            "description": "clear sky",
            "feels_like": 23,
            "humidity": 60,
            "timestamp": 1700000000
        }
        weather_station.fetch_weather("Lviv")
        
        plan1 = mock_db.get_current_plan()
        assert plan1 is not None
        assert plan1['weather']['condition'] == 'Sunny'
        assert any(act['name'] == 'Hiking' for act in plan1['activities'])
        
        mock_get_weather.return_value = {
            "city": "Lviv",
            "condition": "Rainy",
            "temperature": 15,
            "description": "heavy rain",
            "feels_like": 13,
            "humidity": 90,
            "timestamp": 1700003600
        }
        weather_station.fetch_weather("Lviv")
        
        plan2 = mock_db.get_current_plan()
        assert plan2 is not None
        assert plan2['weather']['condition'] == 'Rainy'
        assert any(act['name'] == 'HouseWork' for act in plan2['activities'])
        
        assert plan1['weather']['condition'] != plan2['weather']['condition']
        
        print(" Test 15: Full integration test passed!")
        print("   - Observer Pattern: Weather change triggered DayPlanner update ✓")
        print("   - Strategy Pattern: Sunny → Hiking, Rainy → HouseWork ✓")
        print("   - Plan generation and storage working correctly ✓")

if __name__ == "__main__":
    
    exit_code = pytest.main([
        __file__,
        "-v",
        "-s",
        "--tb=short",
        "--color=yes"
    ])
    
    sys.exit(exit_code)