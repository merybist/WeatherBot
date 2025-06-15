# WeatherBot

**WeatherBot** is a Telegram bot that provides a weekly weather forecast for any city. It supports both English and Ukrainian languages and stores user preferences (language, user ID, and username) in a PostgreSQL database.

## Features

- 5–6 day weather forecast for any city worldwide
- Language switching (English/Ukrainian) with the `/language` command
- Stores user language, ID, and username in PostgreSQL
- Simple and friendly Telegram interface

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/weatherbot.git
cd weatherbot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root and add:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
OPENWEATHER_API_KEY=your_openweather_api_key

user=your_pg_user
password=your_pg_password
host=localhost
port=5432
dbname=weatherbot
```

> **Note:**  
> - `TELEGRAM_BOT_TOKEN` — your Telegram bot token  
> - `OPENWEATHER_API_KEY` — your OpenWeatherMap API key  
> - PostgreSQL connection values must match your database setup

### 4. Initialize the database

The bot will automatically create the `users` table on first run.  
Make sure the `weatherbot` database exists in your PostgreSQL instance.

### 5. Run the bot

```bash
python main.py
```

## Usage

- `/start` — start interacting with the bot
- `/help` — get instructions
- `/language` — change the bot language (English/Ukrainian)
- Just type a city name to get the weather forecast
