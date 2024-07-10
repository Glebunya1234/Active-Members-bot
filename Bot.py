import random
import discord
from discord.ext import commands
from discord.ui import Button, View
import os
from dotenv import load_dotenv, find_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv(find_dotenv())

# Получение токена из переменной окружения
TOKEN = os.getenv('TOKEN')

text_channel_ids = {}


intents = discord.Intents.all()


bot = commands.Bot(command_prefix='!', intents=intents, case_insensitive=True)

@bot.event
async def on_ready():
    print(f'Bot {bot.user} ready')

@bot.event
async def on_voice_state_update(member, before, after):
    await check_voice_state_changes(member.guild, before.channel, after.channel)

async def check_voice_state_changes(guild, before_channel, after_channel):
    global text_channel_ids
    guild_id = guild.id
    if guild_id in text_channel_ids:
        text_channel = bot.get_channel(text_channel_ids[guild_id])
        if text_channel:
            await delete_bot_messages(text_channel)
            await update_voice_channel_states(guild, text_channel, before_channel, after_channel)

async def update_voice_channel_states(guild, text_channel, before_channel, after_channel):
    channels_to_update = set()
    
    if before_channel and before_channel.guild == guild:
        channels_to_update.add(before_channel)
    if after_channel and after_channel.guild == guild:
        channels_to_update.add(after_channel)
    
    for channel in guild.voice_channels:
        if channel.members:
            channels_to_update.add(channel)

    for channel in channels_to_update:
        await send_voice_state_message(channel, text_channel)

async def delete_bot_messages(channel):
    async for message in channel.history(limit=None):
        if message.author == bot.user:
            await message.delete()

async def send_voice_state_message(channel, text_channel):
    users = channel.members
    if users:
        user_list = "\n".join([f"> _**`{user.name}`**_" for user in users])
        message = f"\n_**Currently in the voice channel '{channel.name}':**_\n{user_list}"
        
        invite = await channel.create_invite(max_age=0, max_uses=0, unique=True)
         
        emojis = ["🎉", "🔥", "🎧", "🎵", "💬", "😊"]
        random_emoji = random.choice(emojis)

        button = Button(label=f"Join",emoji=f"{random_emoji}" , url=invite.url)
        view = View()
        view.add_item(button)

        await text_channel.send(message, view=view)
        await text_channel.send("\n ㅤ")


@bot.command()
async def Bot_Help(ctx):
    message = (
        "> _**Command to install a chat for the bot, which will notify participants about active actions in voice channels:**_\n"
        "> _**```!SetChannel```**_"
        "**_`For example: !SetChannel 123456781234` _**"
        
        "\n\n> _**Command to clear all bot messages in the current chat:**_"
        "> _**```!ClsBot```**_"
        "**_`The user's messages will still remain in the chat` _**"
        
        "\n\n> _**Command to get all text channel IDs on the current server:**_\n"
        "> _**```!GetIdAllChannel```**_"
        "**_`Will list all channel IDs and their names`_**"
        
        "\n\n>_**Team,to get a specific ID of the text channel to which the command will be sent:**_\n"
        "> _**```!GetIdThisChannel```**_"
        "**_`Will display the ID and name, for example: Text channel Main, ID: 12313123123` _**"
    )
    await ctx.send(message)




@bot.command()
async def SetChannel(ctx, channel_id):
    global text_channel_ids
    guild_id = ctx.guild.id
    guild_name = ctx.guild.name
    
   
    channel = ctx.guild.get_channel(int(channel_id))
    
    if channel:
        text_channel_ids[guild_id] = int(channel_id)
     
       
        await ctx.send(f'> _**Text channel for bot notifications is set to: `{channel.name}`, ID: `{channel_id}`, for server `{guild_name}`**_')
    else:
        await ctx.send(f'> _**Could not find channel with ID `{channel_id}` on server `{guild_name}`. Please check and try again.**_')




@bot.command()
async def GetIdAllChannel(ctx):

    text_channels = ctx.guild.text_channels
    channel_list = "\n".join([f"Text channel: `{channel.name}`| ID:`{channel.id}`" for channel in text_channels])

    await ctx.send(f">>> _** ## List of text channels on the server: \n{channel_list} **_")

@bot.command()
async def GetIdThisChannel(ctx):

    text_channels = ctx.channel

    await ctx.send(f">>> _** ## Below is the ID of this text channel `{text_channels.name}`: \nID: `{text_channels.id}` **_")


@bot.command()
async def ClsBot(ctx):
 
    await delete_bot_messages(ctx)
   

bot.run(TOKEN)













