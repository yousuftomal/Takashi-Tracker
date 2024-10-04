import discord
import geocoder as geocoder
import phonenumbers
import requests
from discord.ext import commands
from opencage.geocoder import OpenCageGeocode
from phonenumbers import geocoder, carrier

import os
from dotenv import load_dotenv

# ===============================================================================

intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix="/", intents=intents)
bot = commands.Bot(command_prefix="/", intents=intents)

# Load environment variables from .env file
load_dotenv()

# Get the Discord token and OpenCage API key from environment variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENCAGE_API_KEY = os.getenv("OPENCAGE_API_KEY")

@client.event
async def on_ready():
    print("TAKASHI-Tracker is awake!")
    print("-------------------------")


@client.command()
async def track_by_ip(ctx):
    await ctx.send("Put ip address:")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    msg = await client.wait_for("message", check=check)
    ipurl = "http://ip-api.com/json/" + str(msg.content)
    response = requests.get(ipurl).json()
    print(response)
    await ctx.send(f"IP: {msg.content}")
    await ctx.send(f"ISP: {response['isp']}")
    await ctx.send(f"Organization: {response['org']}")
    await ctx.send(f"Country: {response['country']}")
    await ctx.send(f"Region: {response['regionName']}")
    await ctx.send(f"City: {response['city']}")
    await ctx.send(f"Latitude: {response['lat']}")
    await ctx.send(f"Longitude: {response['lon']}")

@client.command()
async def track_by_phoneNumber(ctx):
    await ctx.send("Put phonr Number with country code:")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    msg = await client.wait_for("message", check=check)
    print(msg.content)
    ch_number = phonenumbers.parse(msg.content, "CH")
    cdetails = geocoder.description_for_number(ch_number, "en")

    service_name = phonenumbers.parse(msg.content, "RO")
    sdetails = carrier.name_for_number(service_name, "en")

    print(cdetails)
    print(sdetails)

    geo = OpenCageGeocode(OPENCAGE_API_KEY)
    query = str(cdetails)
    results = geo.geocode(query)
    print(results[2])


client.run(DISCORD_TOKEN)