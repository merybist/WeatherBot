import requests
from datetime import datetime
import os
from dotenv import load_dotenv
import locale

load_dotenv()

ERROR_TEXTS = {
    'uk': {
        'auth': 'Помилка автентифікації API. Перевірте ваш API ключ.',
        'not_found': "Місто '{city}' не знайдено. Перевірте правильність написання.",
        'api': 'Помилка при отриманні прогнозу погоди. Спробуйте пізніше.',
        'network': 'Помилка мережі: {err}',
        'unexpected': 'Сталася помилка: {err}',
        'title': '🌤 Прогноз погоди для міста {city}:'
    },
    'en': {
        'auth': 'API authentication error. Check your API key.',
        'not_found': "City '{city}' not found. Please check the spelling.",
        'api': 'Error getting weather forecast. Please try again later.',
        'network': 'Network error: {err}',
        'unexpected': 'An error occurred: {err}',
        'title': '🌤 Weather forecast for {city}:'
    }
}

LABELS = {
    'uk': {
        'date': '📅 {date}:',
        'temp': '🌡 Температура: {min:.1f}°C - {max:.1f}°C',
        'desc': '☁️ {desc}',
        'humidity': '💧 Вологість: {humidity}%',
        'wind': '💨 Швидкість вітру: {wind} м/с',
        'date_fmt': '%d.%m.%Y',
    },
    'en': {
        'date': '📅 {date}:',
        'temp': '🌡 Temperature: {min:.1f}°C - {max:.1f}°C',
        'desc': '☁️ {desc}',
        'humidity': '💧 Humidity: {humidity}%',
        'wind': '💨 Wind speed: {wind} m/s',
        'date_fmt': '%B %d, %Y',
    }
}

class WeatherHandler:
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        if not self.api_key:
            raise ValueError("OPENWEATHER_API_KEY не знайдено в змінних середовища")
        self.base_url = "http://api.openweathermap.org/data/2.5/forecast"

    def get_weather_forecast(self, city, lang='uk'):
        try:
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric',
                'lang': lang
            }
            response = requests.get(self.base_url, params=params)
            if response.status_code != 200:
                if response.status_code == 401:
                    return ERROR_TEXTS[lang]['auth']
                elif response.status_code == 404:
                    return ERROR_TEXTS[lang]['not_found'].format(city=city)
                else:
                    return ERROR_TEXTS[lang]['api']
            data = response.json()
            daily_forecasts = {}
            for item in data['list']:
                date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
                if date not in daily_forecasts:
                    daily_forecasts[date] = {
                        'temp_min': float('inf'),
                        'temp_max': float('-inf'),
                        'description': item['weather'][0]['description'],
                        'humidity': item['main']['humidity'],
                        'wind_speed': item['wind']['speed']
                    }
                daily_forecasts[date]['temp_min'] = min(daily_forecasts[date]['temp_min'], item['main']['temp_min'])
                daily_forecasts[date]['temp_max'] = max(daily_forecasts[date]['temp_max'], item['main']['temp_max'])
            return self._format_forecast(daily_forecasts, city, lang)
        except requests.exceptions.RequestException as e:
            return ERROR_TEXTS[lang]['network'].format(err=str(e))
        except Exception as e:
            return ERROR_TEXTS[lang]['unexpected'].format(err=str(e))

    def _format_forecast(self, daily_forecasts, city, lang):
        formatted_forecast = f"{ERROR_TEXTS[lang]['title'].format(city=city)}\n\n"
        labels = LABELS[lang]
        if lang == 'en':
            try:
                locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')
            except:
                pass
        for date, forecast in daily_forecasts.items():
            formatted_date = datetime.strptime(date, '%Y-%m-%d').strftime(labels['date_fmt'])
            formatted_forecast += (
                labels['date'].format(date=formatted_date) + "\n" +
                labels['temp'].format(min=forecast['temp_min'], max=forecast['temp_max']) + "\n" +
                labels['desc'].format(desc=forecast['description'].capitalize()) + "\n" +
                labels['humidity'].format(humidity=forecast['humidity']) + "\n" +
                labels['wind'].format(wind=forecast['wind_speed']) + "\n\n"
            )
        return formatted_forecast
