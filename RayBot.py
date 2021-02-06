import discord
from discord.ext import commands
import random
import datetime
import discord.utils
import os
# import logging
from ahelp import adv_help, aliases, mod_help

intents = discord.Intents().all()
bot = commands.Bot(command_prefix=commands.when_mentioned_or('>'), intents=intents)
glodalt = datetime.datetime.now()
bot.remove_command('help')


# logging.basicConfig(level=logging.DEBUG)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(name='for >help', type=discord.ActivityType.watching))
    print('Bot ready!')


@bot.command(name='ping')  # Regular ping command to check response latency.
async def ping(ctx):
    await ctx.send(f'Pong! Response latency is: {round(bot.latency * 1000)} ms!')


@bot.command(name='help')  # Shows bot's commands, duh.
async def help(ctx, command=None):
    Help_Embed = discord.Embed(color=0xfdcf92)
    if not command:
        Help_Embed.set_author(name='List of all available commands(W.I.P)',
                              icon_url='https://tinyurl.com/1fz6h0dv'
                              )
        Help_Embed.add_field(name='🔨Utility',
                             value='`help` `avatar` `ping` `ui`',
                             inline=False)
        Help_Embed.add_field(name='🎲Fun stuff',
                             value='`8ball` `coinflip` `do`',
                             inline=False)
        Help_Embed.add_field(name="🤖 Warframe info",
                             value="`news` `cetus` `nightwave` `baro` `cetus` `vallis` `cambion`\n"
                                   "`sortie`",
                             inline=False)
        Help_Embed.set_footer(text="For moderation commands, see >mhelp | Type >help <command> for more info")
        await ctx.send(embed=Help_Embed)
    elif command.lower() in adv_help.keys():
        Help_Embed.set_author(name=f"Command info: {command.lower()}")
        Help_Embed.add_field(name="Description:", value=adv_help.get(command),
                             inline=False)
        Help_Embed.add_field(name="Aliases:", value=aliases.get(command),
                             inline=False)
        await ctx.send(embed=Help_Embed)
    else:
        await ctx.send('No such command found, sad.')


@bot.command(name='mhelp')  # Shows moderation commands
@commands.has_any_role(
    697579282557304933, 648594572401704971, 697585255518961685, 573909157854314526
)
async def mhelp(ctx, command=None):
    Help_Embed = discord.Embed(color=0xa03ca7)
    if not command:
        Help_Embed.set_author(name='List of all moderation commands(W.I.P)',
                              icon_url='https://bit.ly/2LquDwO'
                              )
        Help_Embed.add_field(name='Assignment',
                             value='``assign`` ``name`` ``guest`` ``hiatus`` ``warn``')
        Help_Embed.set_footer(text='For regular commands, see >help')
        await ctx.send(embed=Help_Embed)
    elif command.lower() in mod_help.keys():
        Help_Embed.set_author(name=f"Command info: {command.lower()}")
        Help_Embed.add_field(name="Description:", value=mod_help.get(command),
                             inline=False)
        Help_Embed.add_field(name="Aliases:", value=aliases.get(command),
                             inline=False)
        await ctx.send(embed=Help_Embed)
    else:
        await ctx.send('No such command found, sad.')


@mhelp.error
async def mhelp_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send(
            "This command is moderator-only.", delete_after=3
        )
    else:
        print(error)


@bot.command(aliases=['8ball'])  # Literally just a  boring 8ball command.
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


@bot.command(name='coinflip')  # Flips a coin!
async def coinflip(ctx):
    ht = ['Heads', 'Tails']
    await ctx.send(f'{random.choice(ht)}')


@bot.command(name='assign')  # Assigns a person with a clannie role while removing hiatus/newcomer roles.
@commands.has_any_role(
    697579282557304933, 648594572401704971, 697585255518961685, 573909157854314526
)
async def assign(ctx, member: discord.Member):
    user = ctx.message.author.id
    memberid = member.id
    if memberid == user:
        await ctx.send("Can't use this command on yourself.")
    else:
        # ━━━━━Fetches roles to add/remove. Extremely inefficient━━━━━
        roleAdd = member.guild.get_role(573966506644471819)
        roleRemove = member.guild.get_role(618114983737425931)
        roleRemove1 = member.guild.get_role(689438890313908255)
        roleActivity = member.guild.get_role(729056392232697887)
        roleOptIn = member.guild.get_role(729036706690629772)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        channel = bot.get_channel(689592463010168849)
        welcome = bot.get_channel(573908464087334924)
        time = datetime.datetime.now()
        embed = discord.Embed(description='Done!', color=0x4cff30)
        logembed = discord.Embed(timestamp=ctx.message.created_at,
                                 description=f'<@{member.id}>({member.id}) was assigned by <@{ctx.message.author.id}>',
                                 color=0xa03ca7
                                 )
        logembed.set_footer(text=f"Cephalon Ray")
        await member.remove_roles(roleRemove, roleRemove1)
        await member.add_roles(roleAdd, roleActivity, roleOptIn)
        await ctx.send(embed=embed, delete_after=3)
        await channel.send(embed=logembed)
        await welcome.send(f"Welcome, <@{member.id}> ❤️")


@assign.error
async def assign_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send(
            "This command is mod-only.", delete_after=3
        )
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify the member.", delete_after=3)
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Invalid member.", delete_after=3)
    else:
        print(error)
        await ctx.send("Something went wrong. Blame Akarui for coding:/")


@bot.command(name='name')  # Adds ✨ in front of user's name.
@commands.has_any_role(
    697579282557304933, 648594572401704971, 697585255518961685, 573909157854314526
)
async def name(ctx, member: discord.Member, *, nickname=None):
    initialName = member.display_name
    user = ctx.message.author.id
    memberid = member.id
    if memberid == user:
        await ctx.send("Can't use this command on yourself.")
    else:
        channel = bot.get_channel(689592463010168849)
        Emoji = '✨ '
        time = datetime.datetime.now()
        embed = discord.Embed(description='Done!', color=0x4cff30)
        logembed = discord.Embed(timestamp=ctx.message.created_at,
                                 description=f'<@{member.id}>({member.id}) has recieved a name change from <@{ctx.message.author.id}>',
                                 color=0xa03ca7
                                 )
        logembed.set_footer(text=f"Cephalon Ray")
        await member.edit(nick=Emoji + nickname)
        await ctx.send(embed=embed, delete_after=3)
        await channel.send(embed=logembed)


@name.error
async def name_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("This command is mod-only.", delete_after=3)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify the member.", delete_after=3)
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Invalid member.", delete_after=3)
    else:
        print(error)
        await ctx.send("Something went wrong. Blame Akarui for bad coding:/")


@bot.command(name='avatar')  # Fetches an avatar of a person.
async def avatar(ctx, member: discord.Member = None):
    if not member:
        member = ctx.message.author
    embed = discord.Embed(description=f"**Profile picture of:** <@{member.id}>", color=0xfdcf92,
                          timestamp=ctx.message.created_at)
    embed.set_image(url=member.avatar_url)
    await ctx.send(embed=embed)


@avatar.error
async def avatar_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send(
            'Invalid user.', delete_after=3
        )
    else:
        print(error)


@bot.command(name='guest')  # Reverts user back to Server Guest role
@commands.has_any_role(
    697579282557304933, 648594572401704971, 697585255518961685, 573909157854314526
)
async def guest(ctx, member: discord.Member):
    user = ctx.message.author.id
    memberid = member.id
    if memberid == user:
        await ctx.send("Can't use this command on yourself.")
    else:
        embed = discord.Embed(color=0x4cff30, description='Done!')
        channel = bot.get_channel(689592463010168849)
        nl = '\n'
        logembed = discord.Embed(color=0xa03ca7, timestamp=ctx.message.created_at,
                                 description=f'<@{member.id}>({member.id}) recieved ``Server Guest`` role from <@{ctx.message.author.id}>')
        Guest = member.guild.get_role(689438890313908255)
        Clannie = member.guild.get_role(573966506644471819)
        await member.add_roles(Guest)
        await member.remove_roles(Clannie)
        await ctx.send(embed=embed, delete_after=3)
        await channel.send(embed=logembed)


@bot.command(name='hiatus')  # Removes person's clannie role and gives them a Hiatus role.
@commands.has_any_role(
    697579282557304933, 648594572401704971, 697585255518961685, 573909157854314526
)
async def hiatus(ctx, member: discord.Member):
    user = ctx.message.author.id
    memberid = member.id
    if memberid == user:
        await ctx.send("Can't use this command on yourself.")
    else:
        embed = discord.Embed(color=0x4cff30, description='Done!')
        channel = bot.get_channel(689592463010168849)
        time = datetime.datetime.now()
        logembed = discord.Embed(color=0xa03ca7,
                                 description=f'<@{member.id}>({member.id}) was removed from the clan by <@{ctx.message.author.id}>',
                                 timestamp=ctx.message.created_at)
        logembed.set_footer(text=f"Cephalon Ray")
        Break = member.guild.get_role(618114983737425931)
        Clannie = member.guild.get_role(573966506644471819)
        await member.remove_roles(Clannie)
        await member.add_roles(Break)
        await ctx.send(embed=embed, delete_after=3)
        await channel.send(embed=logembed)


@hiatus.error
async def hiatus_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("This command is mod-only.", delete_after=3)
    else:
        print(error)


@bot.command(name='wl')  # Assigns a warlord.
@commands.is_owner()
async def warlord(ctx, member: discord.Member):
    embed = discord.Embed(color=0x4cff30, description='Done!')
    wl = member.guild.get_role(697579282557304933)
    mod = member.guild.get_role(697585255518961685)
    rec = member.guild.get_role(648594572401704971)
    emoji = '💠'
    name = member.nick
    await member.add_roles(wl, mod, rec)
    await member.edit(nick=emoji + name[1:])
    await ctx.send(embed=embed, delete_after=3)


@warlord.error
async def wl_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("This command is owner only.", delete_after=3)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify the member.", delete_after=3)
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Invalid member.", delete_after=3)
    else:
        print(error)
        await ctx.send("Something went wrong. Blame Akarui for bad coding:/")


@bot.command(name='mod')  # Assigns a moderator.
@commands.is_owner()
async def mod(ctx, member: discord.Member):
    embed = discord.Embed(color=0x4cff30, description='Done!')
    mod = member.guild.get_role(697585255518961685)
    rec = member.guild.get_role(648594572401704971)
    emoji = '🐦'
    name = member.nick
    await member.edit(nick=emoji + name[1:])
    await member.add_roles(mod, rec)
    await ctx.send(embed=embed, delete_after=3)


@mod.error
async def mod_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("This command is owner only.", delete_after=3)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify the member.", delete_after=3)
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Invalid member.", delete_after=3)
    else:
        print(error)
        await ctx.send("Something went wrong. Blame Akarui for bad coding:/")


@bot.command(name='recruiter', aliases=['rec'])  # Assgins a recruiter.
@commands.is_owner()
async def rec(ctx, member: discord.Member):
    embed = discord.Embed(color=0x4cff30, description='Done!')
    rec = member.guild.get_role(648594572401704971)
    emoji = '🦄'
    name = member.nick
    await member.edit(nick=emoji + name[1:])
    await member.add_roles(rec)
    await ctx.send(embed=embed, delete_after=3)


@rec.error
async def rec_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("This command is owner only.", delete_after=3)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify the member.", delete_after=3)
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Invalid member.", delete_after=3)
    else:
        print(error)
        await ctx.send("Something went wrong. Blame Akarui for bad coding:/")


@bot.command(name='warn')  # Warns a person about being inactive in Warframe.
@commands.has_any_role(
    697579282557304933, 648594572401704971, 697585255518961685, 573909157854314526
)
async def warn(ctx, member: discord.Member):
    embed = discord.Embed(color=0x4cff30, description='Done!')
    user = ctx.message.author.id
    target = member.id
    channel = bot.get_channel(689592463010168849)
    logembed = discord.Embed(color=0xa03ca7, timestamp=ctx.message.created_at,
                             description=f'<@{member.id}>({member.id}) was reminded to log in by <@{ctx.message.author.id}>')
    logembed.set_footer(text=f"Cephalon Ray")
    if user == target:
        await ctx.send("Can't really warn yourself bud", delete_after=3)
    else:
        await member.send(f"""Hello {member.name}, Blossoming Serenity bot here 🙂
\nYou have recieved this message due to being offline for almost **14 Days** in Warframe.
Please, log-in as soon as possible to avoid being kicked from the clan.
\n**If you can't log in or are taking a break**: let a Warlord or Moderator know about it.\nThank you! 💙""")
        await ctx.send(embed=embed, delete_after=3)
        await channel.send(embed=logembed)


@warn.error
async def name_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("This command is mod-only.", delete_after=3)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify the member.", delete_after=3)
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Invalid member.", delete_after=3)
    else:
        print(error)
        await ctx.send("Something went wrong. Blame Akarui for bad coding:/")


@bot.command(name='userinfo', aliases=['ui'])  # Shows info about the targeted user.
async def user(ctx, member: discord.Member = None):
    if not member:
        member = ctx.message.author  # Shows message author's info when no target is specified.

    # ━━━Fetches current time and date, as well as date when a user created an account and joined the server.━━
    now = datetime.datetime.now().date()
    date2 = member.joined_at.date()
    date3 = member.created_at.date()
    # ━━━━Counts days since server join and account registration━━━━
    c_diff = abs(now - date3).days
    j_diff = abs(now - date2).days
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    roles = [role.mention for role in member.roles[1:]]
    # ━━━━Builds the embed to send as an output━━━━
    embed = discord.Embed(color=0xffa07a, title=f'User info of {member.name}', timestamp=ctx.message.created_at)
    embed.add_field(name='User ID:', value=member.id, inline=False)
    embed.add_field(name='Display name:', value=member.display_name)
    embed.add_field(name='Joined at:',
                    value=member.joined_at.strftime(f"%a, %#d %B %Y, %I:%M %p UTC ({j_diff} days ago)"),
                    inline=False)
    embed.add_field(name='Account created at:', value=member.created_at.strftime(
        f"%a, %#d %B %Y, %I:%M %p UTC ({c_diff} days ago)"),
                    inline=False)
    embed.add_field(name="Roles:", value='   '.join(roles), inline=False)
    embed.add_field(name="Top role:", value=member.top_role.mention, inline=False)
    embed.add_field(name="Current status:", value=f'{member.status}', inline=True)
    if member.activity == None:
        embed.add_field(name="Current Activity:", value=member.activity,
                        inline=True)  # Prevents NoneType error thingy(tm) when user has no activity set.
    else:
        embed.add_field(name="Current Activity:", value=member.activity.name, inline=True)
    if member.bot:  # Checks if a target is a human or a bot.
        embed.add_field(name='Bot/Human:', value='Bot', inline=True)
    else:
        embed.add_field(name='Bot/Human:', value='Human', inline=True)
    embed.set_footer(text='Cephalon Ray')
    await ctx.send(embed=embed)


@bot.command(name='do')  # "action" command. User "does" something
async def do(ctx, *, msg):
    auth = ctx.message.author
    await ctx.message.delete()
    await ctx.send(f'**{auth.display_name}** ' + msg)


with open('token.txt') as token_file:
    token = token_file.read().strip()

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(token)
