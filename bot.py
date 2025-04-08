import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import weather

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
async def get_forcast(ctx, zip_code=None):
    """Get forecast for a zip code or saved default"""

 # Check if no zip code provided
    if not zip_code:
        await ctx.send("Please provide a zip code")
        return
    
    # Get weather data
    data = weather.get_forcast(zip_code)
    
    print(data)

    # Check if there was an error
    if "error" in data:
        await ctx.send(data["error"])
        return
    
    # Create embed for formatting
    embed = discord.Embed(
        title=f"Weather for {data['city']}",
        description=f"Forecast for: {data['description']}",
        color=0x00AAFF
    )
    
    # TODO: create embed display in github
    
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