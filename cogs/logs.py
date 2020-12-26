import datetime
import discord
from discord.ext import commands

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel = 689592463010168849

    @commands.Cog.listener()
    async def on_member_join(self, member):
        log_embed = discord.Embed(color = 0xa03ca7, title = f"{member} has joined the server",
        timestamp = datetime.datetime.now())
        date = member.created_at.date()
        now = datetime.datetime.now().date()
        acc_created = abs(now-date).days
        log_embed.add_field(name = "User ID:", value = member.id, inline = False)
        if acc_created < 30:
            log_embed.add_field(name = "Account created at:", value = date.strftime(f"%#d %B %Y ({acc_created} days ago, **New Account**)"))
        else:
            log_embed.add_field(name = "Account created at:", value = date.strftime(f"%#d %B %Y ({acc_created} days ago)"))
        log_embed.set_thumbnail(url = member.avatar_url)
        log_embed.set_footer(text = 'Cephalon Ray')
        await self.bot.get_channel(self.log_channel).send(embed=log_embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        log_embed = discord.Embed(color = 0xa03ca7, title = f"{member} has left the server",
        timestamp = datetime.datetime.now())
        now = datetime.datetime.now().date()
        date = member.joined_at.date()
        first_joined = abs(now-date).days
        log_embed.add_field(name = "User ID:", value = member.id, inline = False)
        log_embed.add_field(name = "Server nick:", value = member.nick, inline = False)
        log_embed.add_field(name = "Joined at:", value = date.strftime(f"%#d %B %Y ({first_joined} days ago)"))
        log_embed.set_thumbnail(url = member.avatar_url)
        log_embed.set_footer(text = 'Cephalon Ray')
        await self.bot.get_channel(self.log_channel).send(embed=log_embed)

def setup(bot):
    bot.add_cog(Logs(bot))
