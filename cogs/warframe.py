import discord
from discord.ext import commands
from datetime import datetime
import aiohttp
import atexit


class Warframe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def wfstat(self, name):
        async with aiohttp.ClientSession() as self.session:
            async with self.session.get("https://api.warframestat.us/pc/" + name) as resp:
                return await resp.json()

    # @commands.Cog.listener()
    # async def on_disconnect(self):
    #     print("bye lol")

    @commands.command()
    async def news(self, ctx):
        news_embed = discord.Embed(color=0x0081a2, title="Warframe News", timestamp=ctx.message.created_at)
        for article in await self.wfstat("news"):
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
        for challenge in (await self.wfstat("nightwave"))["activeChallenges"]:
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
        for baro in await self.wfstat("voidTrader"):
            baro_embed.add_field(name="Arrives in", value=baro["startString"], inline=False)
            baro_embed.add_field(name="Relay:", value=baro["location"], inline=False)
            if not baro["inventory"]:
                baro_embed.add_field(name="Inventory", value="Baro Ki'Teer is yet to arrive.", inline=False)
            else:
                for item in baro["inventory"]:
                    ducats = item["ducats"]
                    creds = item["credits"]
                    item_name = item["item"]
                    baro_embed.add_field(name=item_name, value=f"{ducats} <:Ducats:573969761109803056> +\n"
                                                               f"{creds} <:Credits:573969762099527684>")
        baro_embed.set_thumbnail(url="https://tinyurl.com/2bmp8vd7")
        baro_embed.set_footer(text="Cephalon Ray")
        await ctx.send(embed=baro_embed)
        await self.session.close()

    @commands.command(name="cetus")
    async def cetus(self, ctx):
        cetus_embed = discord.Embed(title="Cetus state", color=discord.Colour.green(),
                                    timestamp=ctx.message.created_at)
        # yes, implementation is shit, I know.
        for time_request in await self.wfstat("cetusCycle"):
            for bounties_request in await self.wfstat("syndicateMissions"):
                time_left = time_request["shortString"]
                ostron_syndicate = bounties_request[0]
                if time_request["isDay"]:
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
        async with self.wfstat("vallisCycle") as time_request:
            async with self.wfstat("syndicateMissions") as bounties_request:
                vallis_syndicate = bounties_request[2]
                time_left = time_request["shortString"]
                if time_request["isWarm"]:
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
        for jobs in (await self.wfstat("syndicateMissions"))[1]["jobs"]:
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
        async with self.wfstat("sortie") as sortie:
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



