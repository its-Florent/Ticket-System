import discord
import asyncio
from discord.ext import commands



bot = commands.Bot(command_prefix='.')

@bot.event  # Ready Event
async def on_ready():
    print("Bot Online mit:")
    print("Username: ", bot.user.name)
    print("User ID: ", bot.user.id)
    bot.loop.create_task(status_task())


async def status_task():
    while True:
        await bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.streaming, name=f'𝐺𝐴𝑀𝐼𝑁𝐺-𝑍𝑂𝑁𝐸',
                                      url="https://www.twitch.tv/#"))
        await asyncio.sleep(60)



CHANNEL_ID = 765965980048162828 # Wo ist die Reaction
GUILD_ID = 697213730420818002 # Dein Serverid
ROLE_1 = 710109933089325136 # Team Rolle / kannst auch mehrere z.b:
#ROLE_2 = 1231231231123
CATEGORY_ID = 765965896505229352 # Wo soll das Ticket erstellet werden btw welche Category.


@bot.event
async def on_raw_reaction_add(payload):
    if payload.member.bot:
        return
    if payload.channel_id == CHANNEL_ID:
        channel = bot.get_channel(CHANNEL_ID)
        guild = bot.get_guild(payload.guild_id)
        user = bot.get_user(payload.user_id)
        message = await channel.fetch_message(payload.message_id)
        await message.remove_reaction(payload.emoji, user)
        for tickets in guild.channels:
            if str(user.id) in tickets.name:
                embed = discord.Embed(title="Ticket Limit erreicht!",
                                      description=f'Du kannst immer nur ein Ticket offen haben! {tickets.mention}!',
                                      color=16711680)
                try:
                 await user.send(embed=embed)#
                except:
                    pass
                return

        category = bot.get_channel(CATEGORY_ID)
        ticket_channel = await guild.create_text_channel(f"🎟️-ticket-{user.id}", category=category,
                                                         topic=f"Ticket-System made by its_florent")
        await ticket_channel.set_permissions(guild.get_role(guild.id), send_messages=False,
                                             read_messages=False)
        await ticket_channel.set_permissions(user, send_messages=True, read_messages=True, add_reactions=False,
                                             embed_links=True, attach_files=True, read_message_history=True,
                                             external_emojis=True)
        await ticket_channel.set_permissions(guild.get_role(ROLE_1), send_messages=True, read_messages=True,
                                             add_reactions=False,
                                             embed_links=True, attach_files=True, read_message_history=True,
                                             external_emojis=True)
        embed = discord.Embed(description=f'Willkommen im Ticket {user.mention}\n'
                                          f'Ein Moderator oder Supporter wird dir in wenigen Minuten helfen!\n'
                                          f'Zum schließen kannst du ❌ verwenden.',
                              color=62719)
        embed.set_author(name=f'Neues Ticket')
        await ticket_channel.send(f"{user.mention}")
        mess_2 = await ticket_channel.send(embed=embed)
        await mess_2.add_reaction('❌')
        embed = discord.Embed(title="Ticket geöffnet!",
                              description=f'Dein Support Ticket wurde geöffnet.',
                              color=discord.colour.Color.green())
        try:
         await user.send(embed=embed)
        except:
            pass
        return
    if payload:
        channel = bot.get_channel(payload.channel_id)
        if '🎟️-ticket-' in channel.name:
             user = bot.get_user(payload.user_id)
             embed = discord.Embed(
                description=f'Das Ticket wurde geschlossen und in 5s gelöscht!',
                color=16711680)
             await channel.send(embed=embed)
             await asyncio.sleep(5)
             await channel.delete()




bot.run('NzE1NTU2MTUzMDk4MjQwMDQx.Xs-7mQ.wBAHMsdgocf1eNnYBGv3Z-YA0KU')# Token
