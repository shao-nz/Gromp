import discord
from discord import app_commands
from discord.ext import commands

import json
import requests
import utils

import os
from dotenv import load_dotenv
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

RIOT_SERVICE_BASEURL = "http://localhost:8000/"

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

gromp = commands.Bot(command_prefix="~", intents=intents)


@gromp.event
async def on_ready():
    print(f"Logged on as {gromp.user}!")
    await gromp.tree.sync()
    print("Synced commands")


@gromp.hybrid_command(name="live", with_app_command=True, description="Live game information")
@app_commands.describe(
    summoner="Summoner name"
)
async def live(ctx, summoner):
    await ctx.interaction.response.defer()

    blue_team = list()
    red_team = list()
    msg = ""

    url = f"{RIOT_SERVICE_BASEURL}api/riot/summoner/{summoner}"
    r = requests.get(url, verify=False)
    if r.status_code != requests.codes.ok:
        await ctx.interaction.followup.send(f"Summoner {summoner} not found!")
        return

    summoner_data = json.loads(r.json())
    summoner_id = summoner_data["id"]
    summoner_name = summoner_data["name"]

    url1 = f"{RIOT_SERVICE_BASEURL}api/riot/currentGameInfo/{summoner_id}"
    r1 = requests.get(url1, verify=False)

    if r1.status_code != requests.codes.ok:
        await ctx.interaction.followup.send(f"Summoner {summoner} is not in game.")
        return

    game_data = json.loads(r1.json())

    with open("lol_constants/maps.json") as f:
        maps = json.load(f)

    with open("lol_constants/champion.json") as f:
        champs = json.load(f)["data"]

    try:
        participants = game_data["participants"]
        for participant in participants:
            curr_name = participant["summonerName"]
            champ = next(champ for champ in champs if champs[champ]["key"] == str(
                participant["championId"]))
            champ_emote = next(
                f"<:{emote.name}:{emote.id}>" for emote in gromp.emojis if emote.name == champ)
            if participant["teamId"] == 100:
                blue_team.append(f"{champ_emote} {curr_name}")
            else:
                red_team.append(f"{champ_emote} {curr_name}")

        map_name = [map for map in maps if map["mapId"]
                    == game_data["mapId"]][0]["mapName"]
        map_id = str(game_data["mapId"])
        game_mode = game_data["gameMode"]

    except KeyError:
        await ctx.interaction.followup.send(f"{summoner_name} is not in game.")
        return

    msg = f"Currently playing {map_name}, {game_mode}"
    live_deets = discord.Embed(title=f"{summoner_name}",
                               description=msg,
                               color=0xff00ff)
    live_deets.set_thumbnail(url=utils.get_game_icon_path(map_id, game_mode))
    live_deets.add_field(name="Blue Team",
                         value="\n".join(blue_team),
                         inline=True)
    live_deets.add_field(name="Red Team",
                         value="\n".join(red_team),
                         inline=True)
    live_deets.set_image(url=utils.get_parties_bg_path(map_id, game_mode))

    await ctx.interaction.followup.send(embed=live_deets)

gromp.run(DISCORD_TOKEN)