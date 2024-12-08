import os
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from discord.ext import commands

# Spotify Authorization
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope="user-read-playback-state",
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri="http://127.0.0.1:9090"
))

# Discord Bot Setup
bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def nowplaying(ctx):
    playback = sp.current_playback()
    if playback and playback.get("is_playing"):
        song_name = playback["item"]["name"]
        artists = ", ".join(artist["name"] for artist in playback["item"]["artists"])
        await ctx.send(f"Now Playing: {song_name} by {artists}")
    else:
        await ctx.send("Nothing is playing right now.")

bot.run(os.getenv("DISCORD_TOKEN"))