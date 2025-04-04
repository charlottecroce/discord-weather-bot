# discord-weather-bot
CSI160 - Final Project

Charlotte Croce, Eugene Jiang

## Installation

### Set up virtual environment
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Create .env file to store API keys
```
DISCORD_TOKEN=copy-api-key-here
WEATHER_API_KEY=copy-api-key-here
```

### Get Discord Bot Token:
- Go to the [Discord Developer Portal](https://discord.com/developers/applications)
- Create a New Application > Add a Bot
- Go to the "Bot" section in the sidebar
  - Generate/Reset token & copy the token to the `.env` file
  - Scroll down to "Privileged Gateway Intents" and enable the "Message Content Intent" toggle

### OpenWeatherMap API Key:
- Register at [OpenWeatherMap](https://openweathermap.org/api)
- Get your API key from your account at https://home.openweathermap.org/api_keys

### Run bot
```bash
python3 bot.py
```

### Add Bot to a Your Server
- Go to the [Discord Developer Portal](https://discord.com/developers/applications)
- Select your application > OAuth2 > URL Generator
  - Select scopes: `bot`
  - Select permissions: `Send Messages`, `Embed Links`, `Read Message History`
  - Copy the generated URL and open it in your browser
- Select your server to add the bot

## Usage
Get weather for a specific zip code
```
!weather 05401
```