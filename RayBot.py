import discord
from discord.ext import commands, tasks
import random
import os
import datetime
import time
import discord.utils
from discord.utils import get
from itertools import cycle
from datetime import timezone, tzinfo, timedelta
import time as timeModule


bot = commands.Bot(command_prefix = commands.when_mentioned_or('>'))
glodalt = datetime.datetime.now()
bot.remove_command('help')

@bot.event
async def on_ready():
    await bot.change_presence(activity = discord.Activity(name ='>help',type = discord.ActivityType.watching))
    print('Bot ready!')

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! Response latency is: {round(bot.latency*1000)} ms!')

@bot.command(name='help')
async def help(ctx):
    Help_Embed = discord.Embed(color = 0xfdcf92)
    Help_Embed.set_author(name = 'List of all available commands(W.I.P)',
     icon_url = 'https://bit.ly/2LquDwO'
     )
    Help_Embed.add_field(name = '🔨Utility', value = '``help`` ``avatar`` ``ping``', inline = True)
    Help_Embed.add_field(name = '🎲Fun stuff', value = '``8ball`` ``coinflip``', inline = True)
    Help_Embed.set_footer(text = 'For moderation commands, see >mhelp')
    await ctx.send(embed=Help_Embed)

@bot.command(name='mhelp')
@commands.has_any_role(
697579282557304933, 648594572401704971, 697585255518961685, 573909157854314526
)
async def mhelp(ctx):
    Mhelp_Embed = discord.Embed(color =0xa03ca7)
    Mhelp_Embed.set_author(name = 'List of all moderation commands(W.I.P)',
     icon_url = 'https://bit.ly/2LquDwO'
     )
    Mhelp_Embed.add_field(name = 'Assignment', value = '``assign`` ``name`` ``strip`` ``hiatus`` ``warn``')
    Mhelp_Embed.set_footer(text = 'For regular commands, see >help')
    await ctx.send(embed=Mhelp_Embed)
@mhelp.error
async def mhelp_error(ctx, error):
  if isinstance(error, commands.CheckFailure):
    await ctx.send(
    "This command is moderator-only.", delete_after = 3
    )
  else:
    print(error)


@bot.command(aliases = ['8ball'])
async def _8ball(ctx, *, question):
    await ctx.message.delete()
    responses = ['It is certain.',
                'It is decidedly so.',
                'Without a doubt.',
                'Yes - definitely.',
                'You may rely on it.',
                'As I see it, yes.',
                'Most likely.',
                'Outlook good.',
                'Yes.',
                'Signs point to yes.',
                'Reply hazy, try again.',
                'Ask again later.',
                'Better not tell you now.',
                'Cannot predict now.',
                'Concentrate and ask again.',
                "Don't count on it.",
                'My reply is no.',
                'My sources say no.',
                'Outlook not so good.',
                'Very doubtful.']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')


@bot.command()
async def coinflip(ctx):
    ht = ['Heads','Tails']
    await ctx.send(f'{random.choice(ht)}')


@bot.command(name='assign')
@commands.has_any_role(
697579282557304933, 648594572401704971, 697585255518961685, 573909157854314526
)
async def assign(ctx, member : discord.Member):
    roleAdd = member.guild.get_role(573966506644471819)
    roleRemove = member.guild.get_role(573909036379013130)
    roleRemove1 = member.guild.get_role(618114983737425931)
    roleActivity = member.guild.get_role(729056392232697887)
    roleOptIn = member.guild.get_role(729036706690629772)
    channel = bot.get_channel(689592463010168849)
    welcome = bot.get_channel(573908464087334924)
    time = datetime.datetime.now()
    embed = discord.Embed(description = 'Done!', color = 0x4cff30)
    logembed = discord.Embed(
    description = f'<@{member.id}>({member.id}) was assigned by <@{ctx.message.author.id}>',
    color = 0xa03ca7
    )
    logembed.set_footer(text = f"Cephalon Ray• {time.strftime('%I:%M')}")
    await member.remove_roles(roleRemove, roleRemove1)
    await member.add_roles(roleAdd, roleActivity, roleOptIn)
    await ctx.send(embed = embed, delete_after = 3)
    await channel.send(embed = logembed)
    await welcome.send(f"Welcome, <@{member.id}> ❤️")
@assign.error
async def avatar_error(ctx, error):
  if isinstance(error, commands.CheckFailure):
    await ctx.send(
    "This command is mod-only.", delete_after = 3
    )
  elif isinstance(error, commands.MissingRequiredArgument):
    await ctx.send("Please specify the member.", delete_after = 3)
  elif isinstance(error, commands.BadArgument):
    await ctx.send("Invalid member.", delete_after = 3)
  else:
    print(error)
    await ctx.send("Something went wrong. Blame Akarui for coding:/")

@bot.command(name='name')
@commands.has_any_role(
697579282557304933, 648594572401704971, 697585255518961685, 573909157854314526
)
async def name(ctx, member: discord.Member, *, nickname = None):
    initialName = member.display_name
    channel = bot.get_channel(689592463010168849)
    Emoji = '✨ '
    time = datetime.datetime.now()
    embed = discord.Embed(description = 'Done!', color = 0x4cff30)
    logembed = discord.Embed(
    description = f'<@{member.id}>({member.id}) has recieved a name change from <@{ctx.message.author.id}>',
    color = 0xa03ca7
    )
    logembed.set_footer(text = f"Cephalon Ray• {time.strftime('%I:%M')}")
    await member.edit(nick = Emoji+nickname)
    await ctx.send(embed=embed, delete_after = 3)
    await channel.send(embed=logembed)
@name.error
async def name_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("This command is mod-only.", delete_after = 3)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify the member.", delete_after = 3)
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Invalid member.", delete_after = 3)
    else:
        print(error)
        await ctx.send("Something went wrong. Blame Akarui for bad coding:/")

@bot.command(name='avatar')
async def avatar(ctx, member: discord.Member):
    embed = discord.Embed(description = f"**Profile picture of:** <@{member.id}>", color = 0xfdcf92)
    embed.set_image (url = member.avatar_url)
    await ctx.send(embed=embed)
@avatar.error
async def avatar_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send(
        'Invalid user.', delete_after = 3
        )
    else:
        print(error)

@bot.command(name='strip')
@commands.has_any_role(
697579282557304933, 648594572401704971, 697585255518961685, 573909157854314526
)
async def strip(ctx, member:discord.Member):
    embed = discord.Embed(color = 0x4cff30, description = 'Done!')
    channel = bot.get_channel(689592463010168849)
    nl = '\n'
    logembed = discord.Embed(color = 0xa03ca7,
    description = f'<@{member.id}>({member.id}) was stripped of all roles by <@{ctx.message.author.id}>')
    Newcomer = member.guild.get_role(573909036379013130)
    RolesList = member.roles
    for i in RolesList:
        if i.name == '@everyone':
            continue
        else:
            await member.remove_roles(i)
    await member.add_roles(Newcomer)
    await ctx.send(embed=embed, delete_after = 3)
    await channel.send(embed=logembed)
@strip.error
async def strip_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("This command is mod-only.", delete_after = 3)
    else:
        print(error)


@bot.command(name='hiatus')
@commands.has_any_role(
697579282557304933, 648594572401704971, 697585255518961685, 573909157854314526
)
async def hiatus(ctx, member:discord.Member):
    embed = discord.Embed(color = 0x4cff30, description = 'Done!')
    channel = bot.get_channel(689592463010168849)
    time = datetime.datetime.now()
    logembed = discord.Embed(color = 0xa03ca7,
    description = f'<@{member.id}>({member.id}) was removed from the clan by <@{ctx.message.author.id}>')
    logembed.set_footer(text = f"Cephalon Ray• {time.strftime('%I:%M')}")
    Break = member.guild.get_role(618114983737425931)
    Clannie = member.guild.get_role(573966506644471819)
    await member.remove_roles(Clannie)
    await member.add_roles(Break)
    await ctx.send(embed=embed, delete_after = 3)
    await channel.send(embed=logembed)
@hiatus.error
async def hiatus_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("This command is mod-only.", delete_after = 3)
    else:
        print(error)

@bot.command(name = 'wl')
@commands.is_owner()
async def warlord(ctx, member: discord.Member):
    embed = discord.Embed(color = 0x4cff30, description = 'Done!')
    wl = member.guild.get_role(697579282557304933)
    mod = member.guild.get_role(697585255518961685)
    rec = member.guild.get_role(648594572401704971)
    await member.add_roles(wl, mod, rec)
    await ctx.send(embed=embed, delete_after = 3)
@warlord.error
async def wl_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("This command is owner only.", delete_after = 3)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify the member.", delete_after = 3)
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Invalid member.", delete_after = 3)
    else:
        print(error)
        await ctx.send("Something went wrong. Blame Akarui for bad coding:/")

@bot.command(name = 'mod')
@commands.is_owner()
async def mod(ctx, member: discord.Member):
    embed = discord.Embed(color = 0x4cff30, description = 'Done!')
    mod = member.guild.get_role(697585255518961685)
    rec = member.guild.get_role(648594572401704971)
    await member.add_roles(mod, rec)
    await ctx.send(embed=embed, delete_after = 3)
@mod.error
async def mod_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("This command is owner only.", delete_after = 3)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify the member.", delete_after = 3)
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Invalid member.", delete_after = 3)
    else:
        print(error)
        await ctx.send("Something went wrong. Blame Akarui for bad coding:/")


@bot.command(name = 'recruiter', aliases = ['rec'])
@commands.is_owner()
async def rec(ctx, member: discord.Member):
    embed = discord.Embed(color = 0x4cff30, description = 'Done!')
    rec = member.guild.get_role(648594572401704971)
    await member.add_roles(rec)
    await ctx.send(embed=embed, delete_after = 3)
@rec.error
async def rec_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("This command is owner only.", delete_after = 3)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify the member.", delete_after = 3)
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Invalid member.", delete_after = 3)
    else:
        print(error)
        await ctx.send("Something went wrong. Blame Akarui for bad coding:/")


@bot.command(name='warn')
@commands.has_any_role(
697579282557304933, 648594572401704971, 697585255518961685, 573909157854314526
)
async def warn(ctx, member:discord.Member):
    embed = discord.Embed(color = 0x4cff30, description = 'Done!')
    user = ctx.message.author.id
    target = member.id
    channel = bot.get_channel(689592463010168849)
    logembed = discord.Embed(color = 0xa03ca7,
    description = f'<@{member.id}>({member.id}) was reminded to log in by <@{ctx.message.author.id}>')
    logembed.set_footer(text = f"Cephalon Ray• {time.strftime('%I:%M')}")
    if user == target:
        await ctx.send("Can't really warn yourself bud", delete_after = 3)
    else:
        await member.send(f"""Hello {member.name}, Blossoming Serenity bot here 🙂
\nYou have recieved this message due to being offline for almost **14 Days** in Warframe.
Please, log-in as soon as possible to avoid being kicked from the clan.
\n**If you can't log in or are taking a break**: let a Warlord or Moderator know about it.\nThank you! 💙""")
        await ctx.send(embed=embed, delete_after = 3)
        await channel.send(embed = logembed)
@warn.error
async def name_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("This command is mod-only.", delete_after = 3)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify the member.", delete_after = 3)
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Invalid member.", delete_after = 3)
    else:
        print(error)
        await ctx.send("Something went wrong. Blame Akarui for bad coding:/")

bot.run(TOKEN)
