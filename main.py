import discord
from discord.ext import commands
from secrets import token_id
import os
import time
import asyncio
import math
import asyncio
from discord import Color


# bot config
intents = discord.Intents.all()
upTime = time.time()
client =  commands.Bot(command_prefix='.', intents=intents)
client.remove_command('help')

#global vars
server_name = "friends"
devMode = False               
helpContinue = "☑️"
helpStop = "❎"
supportCreate = "✋"
supportCategory = "TICKETS"
serverId = 807244661465808957
numOfTickets = 0


missing_req_arg = "You are missing a required arugment, look at the usage above and try again"

# events
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("hi! im a bot"))
    print("Bot is online.")
    channel = client.get_channel(808083925507112960)
    if devMode == False:
        await channel.send("**ALERT:** Bot is online")
    elif devMode == True:
        return
    
@client.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="member")
    channel = client.get_channel(808773981200842822)
    await discord.Member.add_roles(member, role)
    embed = discord.Embed(title='New Member', color=0xf40000)
    embed.add_field(name="New User: ", value=f'{member}', inline=False)
    embed.add_field(name="Welcome message: ", value=f"Hey, {member}! Welcome to {server_name}!")
    await channel.send(embed=embed)


@client.event
async def on_raw_reaction_add(payload):
    bot = 807251404137431121
    emoji = payload.emoji
    channel = await client.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
    if payload.user_id == bot:
        return
    
    if emoji.name == supportCreate and payload.message_id == 809548980689960973:
        global numOfTickets
        guildid = client.get_guild(serverId)
        category = discord.utils.get(guildid.categories, name=supportCategory)
        numOfTickets += 1
        print(numOfTickets)
        await reaction.remove(payload.member)
        channel = await guildid.create_text_channel(f'ticket-{numOfTickets}', overwrites=None, category=category, reason=None)
        await channel.send(f"Hi, {payload.member.mention}! Thank you for contacting the support team at {server_name} One of the members from the support team will be with you shortly! \n\n**NEW TICKET: <@&809812431659728928>**")
        await channel.send(f'\n\n{payload.member.mention}, while you wait, may you please provide a brief description on what the subject of this ticket is for?')
     
           
    
    
    if emoji.name == helpContinue:
        print("Continued Help")

    
@client.event
async def on_message_delete(message):
    logsChannel = client.get_channel(809483574398812160)
    embed = discord.Embed(title="Message deleted", color=0xf40000)
    embed.add_field(name="Message content:", value=f"{message.content}", inline=False)
    embed.add_field(name="Message author:", value=f"{message.author}", inline=False)
    embed.add_field(name="Channel:", value=f"{message.channel}", inline=False)
    await logsChannel.send(embed=embed)
    
    
    
@client.event
async def on_message_edit(before,after):
    logsChannel = client.get_channel(809483574398812160)
    embed = discord.Embed(title="Message edited", color=0xf40000)
    embed.add_field(name="Message content before edit: ", value=f"{before.content}", inline=False)
    embed.add_field(name="Message content after edit: ", value=f"{after.content}", inline=False)
    embed.add_field(name="Message author: ", value=f"{before.author}",inline=False)
    embed.add_field(name="Channel:", value=f"{before.channel}",inline=False)
    
    await logsChannel.send(embed=embed)

#commands
@client.command()
@commands.has_permissions(administrator=True)
async def test(ctx):
    await ctx.send(f'{ctx.author} has issued the test command, checking if elgible for bot status....')
    user = ctx.author
    allowed_user = client.get_user(463016897110343690)
    if user == allowed_user:
        message = await ctx.send(f'{user} has ran the test command with the corect permissions. Direct messaging them bot information...')
        await user.send(f'Bot information: \n**Server name:** {server_name}\n**Bot uptime:** {round(time.time() - upTime)} seconds\n**Dev Mode:** {devMode}')
        await message.add_reaction('☑️')
    else:
        message2 = await ctx.send(f'{user}, you do not have permission to run the test command. If you think this is a mistake, please contact {allowed_user}')
        await message2.add_reaction('❎')





@client.command()
@commands.has_permissions(administrator=True)
async def ban_f(ctx, member: discord.Member, *, arg=None):
    await ctx.author.send(f"Note, this is not a real ban command, you have only fake banned {member}")
    message = await ctx.send(f'{ctx.author} has banned {member} for {arg}.')
    await member.send(f'You have banned in {server_name} for {arg}.')
    await message.add_reaction('☑️')


@client.command()
@commands.has_permissions(administrator=True)
async def addrole(ctx,member: discord.Member,*,arg):
    role =  discord.utils.get(member.guild.roles, name=arg)
    await discord.Member.add_roles(member, role)
    message = await ctx.send(f"{member} has received the role: **{role}**")
    await message.add_reaction('☑️')
    
@client.command()
@commands.has_permissions(administrator=True)
async def removerole(ctx,member: discord.Member,*,arg):
    role =  discord.utils.get(member.guild.roles, name=arg)
    await discord.Member.remove_roles(member, role)
    message = await ctx.send(f"{member} has been removed from the role: **{role}**")
    await message.add_reaction('☑️')


@client.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int):
    logsChannel = client.get_channel(809483574398812160)
    await ctx.channel.purge(limit=amount)
    embed = discord.Embed(title="Channel purged:", color=0xf40000)
    embed.add_field(name="Channel:", value=f"{ctx.channel}", inline=False)
    embed.add_field(name="Purged by:", value=f"{ctx.author}",inline=False)
    embed.add_field(name="Amount of messages deleted:", value=f"{amount}", inline=False)
    await logsChannel.send(embed=embed)


@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, arg):
    logsChannel = client.get_channel(809483574398812160)
    if member == ctx.author:
        await ctx.send("You cannot kick yourself!")
    else:
        embed = discord.Embed(title="Member kicked: ", color=0xf40000)
        embed.add_field(name="Kicked: ", value=f"Reason: {arg}", inline=False)
        embed.add_field(name="User kicked: ", value=f"{member.mention}", inline=False)
        embed.add_field(name="Kicked by: ", value=f'{ctx.author}', inline=False)
        await member.send(f'You have been kicked in {server_name} for **{arg}**!')

        embed2= discord.Embed(title="Member kicked: ", color=0xf40000)
        embed2.add_field(name="Kicked: ", value=f"Reason: {arg}", inline=False)
        embed2.add_field(name="User kicked: ", value=f"{member.mention}", inline=False)
        embed2.add_field(name="Kicked by: ", value=f'{ctx.author}', inline=False)

        await logsChannel.send(embed=embed2)
        message = await ctx.send(embed=embed)
        await message.add_reaction('☑️')
        await member.kick(reason=arg)



@client.command()
@commands.has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member, *, arg):
    logsChannel = client.get_channel(809483574398812160)
    user = member.mention
    embed = discord.Embed(title="Warning issued: ", color=0xf40000)
    embed.add_field(name="Warning: ", value=f'Reason: {arg}', inline=False)
    embed.add_field(name="User warned: ", value=f'{member.mention}', inline=False)
    embed.add_field(name="Warned by: ", value=f'{ctx.author}', inline=False)
    
    embed2 = discord.Embed(title="Warning issued: ", color=0xf40000)
    embed2.add_field(name="Warning: ", value=f'Reason: {arg}', inline=False)
    embed2.add_field(name="User warned: ", value=f'{member.mention}', inline=False)
    embed2.add_field(name="Warned by: ", value=f'{ctx.author}', inline=False)
    
    await logsChannel.send(embed=embed2)
    await member.send(f'You have been warned in {server_name} for **{arg}**!')
    message = await ctx.send(embed=embed)
    await message.add_reaction('☑️')

@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            message = await ctx.send(f'Unbanned {user.mention}')
            await message.add_reaction('☑️')
            return 

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, arg):
    logsChannel = client.get_channel(809483574398812160)
    if member == ctx.author:
        await ctx.send("You cannot ban yourself!")
    else:
        embed = discord.Embed(title='Member banned', color=0xf40000)
        embed.add_field(name='Banned: ', value=f'Reason: {arg} ', inline=False)
        embed.add_field(name='User banned: ', value=f'{member}', inline=False)
        embed.add_field(name='Banned by:', value=f'{ctx.author}', inline=False)
        
        
        embed2 = discord.Embed(title='Member banned', color=0xf40000)
        embed2.add_field(name='Banned: ', value=f'Reason: {arg} ', inline=False)
        embed2.add_field(name='User banned: ', value=f'{member}', inline=False)
        embed2.add_field(name='Banned by:', value=f'{ctx.author}', inline=False)
        
        await logsChannel.send(embed=embed2)
        await member.send(f'You have been banned in {server_name} for **{arg}**!')

        message = await ctx.send(embed=embed)
        await message.add_reaction('☑️')
        await member.ban(reason=arg)



@client.command(aliases=['help', 'commands'])
async def cmds(ctx):
    embed = discord.Embed(title="Dinner Club Commands: ", color=0xf40000)
    embed.add_field(name=".addrole", value="Description: The add role command is to add a role to a user, you need the admin permission for this command.", inline=False)
    embed.add_field(name=".ban", value="Description: This is the command to ban a user, you need the ban members permission for this command", inline=False)
    embed.add_field(name='.kick', value="Description: This is the command to kick a user, you need the kick members permission for this command", inline=False)
    embed.add_field(name='.purge', value="Description: This is the command to purge a channel, you need the manage messages permission for this command", inline=False)
    embed.add_field(name=".unban", value="Description: This is the command to unban a user, you need the ban members permission for this command", inline=False)
    embed.add_field(name=".warn", value="Description: This is the command to warn a user, you need the kick members permission for this command.", inline=False)
    embed.add_field(name=".removerole", value="Description: The remove role command is to add a role to a user, you need the admin permission for this command.", inline=False)
    
    embed.add_field(name="Continue?", value="Please select a reaction, choose the X mark to close or the check mark to continue.",inline=False)
    
    
    message = await ctx.send(embed=embed)
    await message.add_reaction('☑️')
    await message.add_reaction('❎')


    
@client.command(aliases=['ticket-close', 't-close'])
async def ticketclose(ctx: commands.Context):
    if ctx.channel.category and ctx.channel.category.name == "TICKETS":
        embed = discord.Embed(title="Scheduled closure:", color=0xf40000)
        embed.add_field(name="Scheduled closer:", value=f'{ctx.author} has scheduled to close this ticket!', inline=False)
        embed.add_field(name="Time remaining:", value="This ticket will close in 60 seconds.", inline=False)
        await ctx.send(embed=embed)
        await asyncio.sleep(60)
        await ctx.channel.delete()

    

@client.command(aliases=['ticket-rename', 't-rename'])
async def ticketrename(ctx: commands.Context, name_input): 
    if ctx.channel.category and ctx.channel.category.name == "TICKETS":
        name = f"{name_input}-{numOfTickets}"
        await ctx.channel.edit(name=name )
        await ctx.send(f'Ticket name changed to **{name_input}**!')


@client.command(aliases=['ticket-claim', 't-claim'])
async def ticketclaim(ctx):
    if ctx.channel.category and ctx.channel.category.name == "TICKETS":
        embed = discord.Embed(title="Ticket Claimed:", color=Color.green())
        embed.add_field(name="Claimed by:", value=f"{ctx.author}",inline=False)
        embed.add_field(name="PTS Enabled:", value="Support team, remember you must use PTS in order to speak in a claimed ticket, unless you are a senior moderator+.", inline=False)
    
        claimed_message = await ctx.send(embed=embed)
        
   


# Error handling




@addrole.error
async def addrole_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Please use the command correctly!\nUsage:   **.addrole    (mention valid user)    (role)**\n**Error:**     {missing_req_arg}")



@removerole.error
async def removerole_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Please use the command correctly!\nUsage:   **.removerole    (mention valid user)    (role)**\n**Error:**     {missing_req_arg}")


@ban_f.error
async def banfake_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Please use the command correctly!\nUsage:   **.ban_f     (mention valid user)    (reason)**\n**Error:**    {missing_req_arg}")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to run this command!")


@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Please use the command correctly!\nUsage:   **.purge     (number of messages)**\n**Error:**    {missing_req_arg}")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to run this command!")

@test.error
async def test_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Only bot admins can run the bot test command!")


@kick.error
async def kick_error(ctx, error):
    if isinstace(error, commands.MissingPermissions):
        await ctx.send("Only members with the **kick members** permission can execute this command.")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(F"Please use the command correctly!\nUsage:    **.kick      (mention valid user)**\n**Error:**      {missing_req_arg}")


@ban.error
async def ban_error(ctx, error):
    if isinstace(error, commands.MissingPermissions):
        await ctx.send("Only members with the **ban members** permission can execute this command.")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(F"Please use the command correctly!\nUsage:    **.ban      (mention valid user)**\n**Error:**      {missing_req_arg}")

@warn.error
async def warn_error(ctx, error):
    if isinstace(error, commands.MissingPermissions):
        await ctx.send("Only members with the **kick members** permission can execute this command.")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(F"Please use the command correctly!\nUsage:    **.warn      (mention valid user)**\n**Error:**      {missing_req_arg}")

@unban.error
async def unban_error(ctx, error):
    if isinstace(error, commands.MissingPermissions):
        await ctx.send("Only members with the **ban members** permission can execute this command.")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(F"Please use the command correctly!\nUsage:    **.unban      (mention valid user)**\n**Error:**      {missing_req_arg}")



client.run(token_id)
