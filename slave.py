import discord
import asyncio
import math
import random

from discord.ext import commands

import os
from dotenv import load_dotenv
load_dotenv('.env')

client = commands.Bot(command_prefix = "s.",
                      case_insensitive = True,
                      activity = discord.Game(name = 'SLAVE SIMULATOR!'),
                      status = discord.Status.idle
                      )
client.remove_command('help')

@client.event
async def on_ready():
    print('Can I have some bread?')

@client.command()
async def die(ctx):
    if ctx.author.id in [436973854485643264]:
        await ctx.send(f"I know I know, I'm not getting paid {ctx.author.display_name}!")
        await client.logout()

@client.command()
async def ping(ctx):
    await ctx.send(f'``Master, ping is {round(client.latency * 1000)}ms``')

@client.command()
async def about(ctx):
    await ctx.send('Originally I\'m a worker for Mizu in Cookie Cafe but I don\'t get paid so might as well serve you...')

@client.command()
async def dice(ctx):
    responses = ['1',
                '2',
                '3',
                '4',
                '5',
                '6']
    await ctx.send(f':handshake: *rolling the dice* \n\n:game_die: You rolled a {random.choice(responses)}')

@client.command()
async def back(ctx):
    await ctx.send('I\'m back to work for no pay')

# Moderation

@client.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *, reason = 'absobutely no reason'):
    if ctx.author != member:
        await member.ban(reason = reason)
        await ctx.send(f'{member.mention} has been banned by {ctx.author} for {reason}')
    else:
        await ctx.send(f"Why are you like this... You DO know that you cannot ban {ctx.author} because THAT IS LITERALLY DUMB")

@client.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'{user.mention} has been unbanned')
            return

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member, *, reason="No reason provided"):
        await user.kick(reason=reason)

        kick = discord.Embed(
        title=f":boot: Kicked {user.name}!",
        description=f"Reason: {reason}\nBy: {ctx.author.mention}"
        )

        await ctx.message.delete()
        await ctx.channel.send(embed=kick)
        await user.send(embed=kick)

@client.command(pass_context = True)
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member):
        role = discord.utils.get(member.guild.roles, name='Muted')
        await ctx.author.add_roles(member, role)

        embed=discord.Embed(

        title="User Muted!",
        description="**{0}** was muted by **{1}**!".format(member, ctx.message.author),
        colour = discord.Colour(0Xb8f2f2)
        )

        await ctx.send(embed=embed)

        try:
            role = discord.utils.get(member.guild.roles, name='Muted')
            await ctx.author.add_roles(member, role)
        except discord.ext.commands.errors.MissingRequiredArgument:
            await ctx.send('C\'mon mod, please specifiy a user to mute')

        else:
           embed=discord.Embed(

           title="Permission Denied.",
           description="You don't have permission to use this command.",
           colour = discord.Colour(0Xb8f2f2)
           )

           await ctx.send(embed=embed)


@client.command(pass_context = True)
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member):
        role = discord.utils.get(member.guild.roles, name='Muted')
        await ctx.author.remove_roles(role)

        embed=discord.Embed(

        title="User Unmuted!",
        description="**{0}** was muted by **{1}**!".format(member, ctx.message.author),
        colour = discord.Colour(0Xb8f2f2)
        )

        await ctx.send(embed=embed)

# Verification

@client.command()
@commands.is_owner()
async def verifymsg(ctx):

    verify = discord.Embed(
        title = f'Welcome to {ctx.message.guild.name}!',
        colour = discord.Colour(0Xb8f2f2),
        description = '***User Verification to protect from automatic bots***'
    )

    verify.set_author(
        name = f'{ctx.author}',
        icon_url = ctx.author.avatar_url
    )

    verify.add_field(
        name = '__Verification__',
        value = 'Please react to this message with the first emote!'
    )

    verify = await ctx.send(embed = verify)
    await verify.add_reaction('<a:check:829394425460555796>')

@client.event
async def on_reaction_add(reaction, user):
  # Ch = '706018939460911125'
  # if reaction.message.channel.id != Ch:
  #   return
  if reaction.emoji == '<a:check:829394425460555796>':
    Blind = discord.utils.get(user.server.roles, name='Blind')
    await client.add_roles(user, Blind)


client.run(os.getenv('DISCORD_TOKEN'))
