import discord
from discord.ext import commands
import asset_utils
import lol_constants.types as lol_types
import time


class SummonerRunes(discord.ui.Button):
    def __init__(self, summoner, champ, *args, **kwargs, ):
        super().__init__(*args, **kwargs)
        self.summoner = summoner
        self.champ = champ
        self.summoner_name = self.summoner["summonerName"]
        self.champion_id = self.summoner["championId"]
        self.spell1 = self.summoner["spell1Id"]
        self.spell2 = self.summoner["spell2Id"]
        self.perk_ids = self.summoner["perks"]["perkIds"]
        self.perk_style = self.summoner["perks"]["perkStyle"]
        self.perk_sub_style = self.summoner["perks"]["perkSubStyle"]

    async def callback(self, interaction: discord.Interaction):
        start = time.time()

        await interaction.response.defer()

        rune_emoji = [lol_types.LOL_EMOJI[id] for id in self.perk_ids]
        primary_emoji = rune_emoji[:4]
        secondary_emoji = rune_emoji[4:6]
        stat_emoji = rune_emoji[6:]
        spell1_emoji = lol_types.LOL_EMOJI[self.spell1]
        spell2_emoji = lol_types.LOL_EMOJI[self.spell2]

        time_taken = time.time() - start

        rune_deets = discord.Embed(
            title=f"{self.summoner_name}",
            color=0xff00ff)
        rune_deets.set_thumbnail(
            url=asset_utils.get_champion_portrait(self.champion_id))
        rune_deets.add_field(
            name="Summoner Spells", value=f"{spell1_emoji} {spell2_emoji}", inline=False)

        # rune_deets.add_field(name="Runes", value="", inline=False)
        rune_deets.add_field(name="Prim.", value="\n".join(
            primary_emoji), inline=True)
        rune_deets.add_field(name="Sec.", value="\n".join(
            secondary_emoji), inline=True)
        rune_deets.add_field(
            name="Stats", value="\n".join(stat_emoji), inline=True)
        rune_deets.set_footer(
            text="Took {:.2f} seconds".format(time_taken))
        await interaction.followup.send(embed=rune_deets)


class RuneButtons(discord.ui.View):
    def __init__(self, *, timeout=180, summoners):
        super().__init__(timeout=timeout)
        self.summoners = summoners
        self.add_rune_button()

    def add_rune_button(self):
        for i, summoner in enumerate(self.summoners):
            if i < 5:
                button = SummonerRunes(
                    emoji=summoner[0], style=discord.ButtonStyle.blurple, row=0, summoner=summoner[1], champ=summoner[2])
            else:
                button = SummonerRunes(
                    emoji=summoner[0], style=discord.ButtonStyle.red, row=1, summoner=summoner[1], champ=summoner[2])

            self.add_item(button)
