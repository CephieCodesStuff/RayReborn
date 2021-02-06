import discord
import requests
from discord.ext import commands
from datetime import datetime


class Warframe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def news(self, ctx):
        news_embed = discord.Embed(color=0x0081a2, title="Warframe News", timestamp=ctx.message.created_at)
        request = requests.get('https://api.warframestat.us/pc/news')
        news = request.json()
        for article in news:
            url = article["link"]
            title = article["message"]
            date = datetime.strptime(article["date"],
                                     '%Y-%m-%dT%H:%M:%S.%fZ').strftime("%#d %B %Y")
            if "d" in article["eta"]:
                day = article["eta"].find("d")
                eta = article["eta"][0:day]
                news_embed.add_field(name=f"{date} | {eta} Days ago", value=f"[{title}]({url})", inline=False)
            else:
                news_embed.add_field(name="Today!", value=f"[{title}]({url})", inline=False)
            news_embed.set_footer(text="Cephalon Ray")
            news_embed.set_thumbnail(url="https://tinyurl.com/1fz6h0dv")
        await ctx.send(embed=news_embed)

    @commands.command(name="nw", aliases=["nightwave"])
    async def nightwave(self, ctx):
        nw_embed = discord.Embed(color=0x8a0030, title="This week's nightwave", timestamp=ctx.message.created_at)
        request = requests.get("https://api.warframestat.us/pc/nightwave")
        nw = request.json()
        for challenge in nw["activeChallenges"]:
            challenge_title = challenge["title"]
            challenge_desc = challenge["desc"]
            start = datetime.strptime(challenge["activation"],
                                    '%Y-%m-%dT%H:%M:%S.%fZ')
            end = datetime.strptime(challenge["expiry"],
                                    '%Y-%m-%dT%H:%M:%S.%fZ')
            remaining = abs(end.date()-start.date()).days
            if challenge["reputation"] == 1000:  # Because if challenge["isDaily"] doesn't fucking work
                nw_embed.add_field(name=f"[Daily] {challenge_title}",
                                   value=f"{challenge_desc}\n**Time remaining**: {remaining} Days", inline=False)
            if challenge["reputation"] == 4500:
                nw_embed.add_field(name=f"[Weekly] {challenge_title}",
                                   value=f"{challenge_desc}\n**Time remaining**: {remaining} Days", inline=False)
            if challenge["isElite"]:
                nw_embed.add_field(name=f"[Elite Weekly] {challenge_title}",
                                   value=f"{challenge_desc}\n**Time remaining**: {remaining} Days", inline=False)
        nw_embed.set_thumbnail(url="https://tinyurl.com/4r3togwp")
        nw_embed.set_footer(text="Cephalon Ray")
        await ctx.send(embed=nw_embed)

    @commands.command(name="baro")
    async def baro(self, ctx):
        baro_embed = discord.Embed(title="Baro Ki'Teer",color=discord.Colour.gold(), timestamp=ctx.message.created_at)
        request = requests.get("https://api.warframestat.us/pc/voidTrader")
        baro = request.json()
        baro_embed.add_field(name="Arrives in", value=baro["startString"], inline=False)
        baro_embed.add_field(name="Relay:", value=baro["location"], inline=False)
        if not baro["inventory"]:
            baro_embed.add_field(name="Inventory", value="Baro Ki'Teer is yet to arrive.", inline=False)
#       else show what Baro has in stock. Need to wait for him to appear to see what API outputs:(
        baro_embed.set_thumbnail(url="https://tinyurl.com/2bmp8vd7")
        baro_embed.set_footer(text="Cephalon Ray")
        await ctx.send(embed=baro_embed)

    @commands.command(name="cetus")
    async def cetus(self, ctx):
        cetus_embed = discord.Embed(title="Cetus state", color=discord.Colour.green(),
                                    timestamp=ctx.message.created_at)
        request = requests.get("https://api.warframestat.us/pc/cetusCycle")
        bounties_request = requests.get("https://api.warframestat.us/pc/syndicateMissions")
        cetus_bounties = bounties_request.json()
        cetus_time = request.json()
        time_left = cetus_time["shortString"]
        ostron_syndicate = cetus_bounties[0]
        if cetus_time["isDay"]:
            cetus_embed.add_field(name="☀ It's Day!",
                                  value=f"```asciidoc\n= Time Remaining =\n{time_left}\n```", inline=False)
        else:
            cetus_embed.add_field(name="🌙 It's Night!",
                                  value=f"```asciidoc\n= Time Left =\n{time_left}\n```", inline=False)
        cetus_embed.add_field(name="Current Bounties", value="\u200b", inline=False)
        for jobs in ostron_syndicate["jobs"]:
            rewards = jobs["rewardPool"]
            levels = jobs["enemyLevels"]
            job_name = jobs["type"]
            rewards_str = ", ".join(rewards)
            cetus_embed.add_field(name=f"{job_name} | levels {levels[0]} - {levels[1]}",
                                  value=f"```asciidoc\nRewards :: {rewards_str}\n```", inline=False)
        cetus_embed.set_thumbnail(url="https://tinyurl.com/48tbkjpx")
        cetus_embed.set_footer(text="Cephalon Ray")
        await ctx.send(embed=cetus_embed)

    @commands.command(name="vallis")
    async def vallis(self, ctx):
        vallis_embed = discord.Embed(title="Orb Vallis state", color=discord.Colour.blue(),
                                     timestamp=ctx.message.created_at)
        request = requests.get("https://api.warframestat.us/pc/vallisCycle")
        bounties_request = requests.get("https://api.warframestat.us/pc/syndicateMissions")
        vallis_time = request.json()
        vallis_bounties = bounties_request.json()
        vallis_syndicate = vallis_bounties[2]
        time_left = vallis_time["shortString"]
        if vallis_time["isWarm"]:
            vallis_embed.add_field(name="🔥 It's Warm! 🔥",
                                   value=f"```asciidoc\n= Time Remaining =\n{time_left}\n```", inline=False)
        else:
            vallis_embed.add_field(name="❄ It's Cold! ❄",
                                   value=f"```asciidoc\n= Time Remaining =\n{time_left}\n```", inline=False)
        vallis_embed.add_field(name="Current Bounties", value="\u200b")
        for jobs in vallis_syndicate["jobs"]:
            rewards = jobs["rewardPool"]
            levels = jobs["enemyLevels"]
            job_name = jobs["type"]
            rewards_str = ", ".join(rewards)
            vallis_embed.add_field(name=f"{job_name} | levels {levels[0]} - {levels[1]}",
                                   value=f"```asciidoc\nRewards :: {rewards_str}\n```", inline=False)
        vallis_embed.set_thumbnail(url="https://tinyurl.com/3c64jblu")
        vallis_embed.set_footer(text="Cephalon Ray")
        await ctx.send(embed=vallis_embed)

    @commands.command(name="cambion")
    async def cambion(self, ctx):
        cambion_embed = discord.Embed(title="Cambion Drift bounties", color=discord.Colour.orange(),
                                      timestamp=ctx.message.created_at)
#       request = requests.get("https://api.warframestat.us/pc/cambionCycle") // Outdated info from the API, ignoring.
        bounties_request = requests.get("https://api.warframestat.us/pc/syndicateMissions")
        cambion_bounties = bounties_request.json()
        cambion_syndicate = cambion_bounties[1]
        for jobs in cambion_syndicate["jobs"][:6]:
            rewards = jobs["rewardPool"]
            levels = jobs["enemyLevels"]
            job_name = jobs["type"]
            rewards_str = ", ".join(rewards)
            cambion_embed.add_field(name=f"{job_name} | levels {levels[0]} - {levels[1]}",
                                    value=f"```asciidoc\nRewards :: {rewards_str}\n```", inline=False)
        cambion_embed.set_thumbnail(url="https://tinyurl.com/2kyutpls")
        cambion_embed.set_footer(text="Cephalon Ray")
        await ctx.send(embed=cambion_embed)

    @commands.command(name="sortie")
    async def sorties(self, ctx):
        request = requests.get("https://api.warframestat.us/pc/sortie")
        sortie = request.json()
        faction = sortie["faction"]
        mission_no = 0
        sortie_embed = discord.Embed(title=f"Today's Sortie | {faction}", color=discord.Colour.purple(),
                                     timestamp=ctx.message.created_at)
        sortie_embed.add_field(name="Time left", value=sortie["eta"], inline=False)
        for mission in sortie["variants"]:
            modifier = mission["modifier"]
            modifier_desc = mission["modifierDescription"]
            node = mission["node"]
            mission_type = mission["missionType"]
            sortie_embed.add_field(name=f"Mission #{mission_no + 1} | {node}",
                                   value=f"**Mission type:** {mission_type}"
                                         f"\n**Modifier:** {modifier}"
                                         f"\n**Description:** {modifier_desc}", inline=False)
            mission_no += 1
        sortie_embed.set_thumbnail(url="https://tinyurl.com/2jpomv94")
        sortie_embed.set_footer(text="Cephalon Ray")
        await ctx.send(embed=sortie_embed)


def setup(bot):
    bot.add_cog(Warframe(bot))
