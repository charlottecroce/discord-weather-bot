import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import weather
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Setup bot with command prefix and intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')



@bot.command(name='forecast')
async def get_forecast(ctx, zip_code=None):
    """Get forecast for a zip code or saved default"""

 # Check if no zip code provided
    if not zip_code:
        await ctx.send("Please provide a zip code")
        return
    
    # Get weather data
    data = weather.get_forecast(zip_code)
    
    print(data)

    # Check if there was an error
    if "error" in data:
        await ctx.send(data["error"])
        return
    
    # Create embed for formatting
    # Get city from the first day
    city_name = data['day1']['city']
    
    embed = discord.Embed(
        title=f"7-Day Forecast for {city_name}",
        description=f"Weekly weather forecast for {city_name} ({zip_code})",
        color=0x00AAFF
    )
    
    # Day names
    today = datetime.now()
    weekday_names = []
    for i in range(7):
        day = today + timedelta(days=i)
        weekday_names.append(day.strftime("%A"))  # Full weekday name

    # Add fields for each day
    for i in range(1, 8):
        day_key = f'day{i}'
        if day_key in data:
            day_data = data[day_key]
        
            # Create field name with weekday name
            field_name = weekday_names[i-1]
        
            # Format temperature and description
            temp = round(day_data['temp_day'])
            feels_like = round(day_data['feels_like_day'])
            description = day_data['description'].capitalize()
        
            # Get icon for this specific day
            icon_url = f"http://openweathermap.org/img/wn/{day_data['icon']}@2x.png"
        
            # Create field value with weather information and icon
            field_value = (
                f"**{temp}°F** (Feels like: {feels_like}°F)\n"
                f"{description}\n"
                f"Wind: {day_data['wind_speed']} mph | Humidity: {day_data['humidity']}%"
            )
        
            # Add field to embed
            embed.add_field(name=field_name, value=field_value, inline=True)
    
    # Send the embed
    await ctx.send(embed=embed)




@bot.command(name='weather')
async def get_weather(ctx, zip_code=None):
    """Get current weather for a zip code or saved default"""
    
    # Check if no zip code provided
    if not zip_code:
        await ctx.send("Please provide a zip code")
        return
    
    # Get weather data
    data = weather.get_weather(zip_code)
    
    print(data)

    # Check if there was an error
    if "error" in data:
        await ctx.send(data["error"])
        return
    
    # Create embed for formatting
    embed = discord.Embed(
        title=f"Weather for {data['city']}",
        description=f"Current conditions: {data['description']}",
        color=0x00AAFF
    )
    
    # Add weather info fields
    embed.add_field(name="Temperature", value=f"{data['temp']}°F", inline=True)
    embed.add_field(name="Feels Like", value=f"{data['feels_like']}°F", inline=True)
    embed.add_field(name="Humidity", value=f"{data['humidity']}%", inline=True)
    embed.add_field(name="Wind Speed", value=f"{data['wind_speed']} mph", inline=True)
    
    # Add weather icon
    icon_url = f"http://openweathermap.org/img/wn/{data['icon']}@2x.png"
    embed.set_thumbnail(url=icon_url)
    
    await ctx.send(embed=embed)

# Run the bot
bot.run(TOKEN)
