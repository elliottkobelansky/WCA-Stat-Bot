import discord
import parse as pf
import keep_alive
from importlib import reload


with open('token.txt') as f:
    token = f.read()


client = discord.Client()

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(
                                 type=discord.ActivityType.listening,
                                 name='!wca'))
    print('We have loggen in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content.split(" ")

    if message.content.startswith('!wca'):
        if msg[1].lower() in {"wr", "nr", "afr", "nar", "eur",
                              "asr", "er", "sar", "ocr"}:
            await message.channel.send(embed=pf.best_from_rank(msg[1:]))
        elif msg[1].lower() in {"profile", "p", "pf"}:
            await message.channel.send(embed=pf.profile(msg[2:]))
        elif msg[1].lower() == "wrs":
            await message.channel.send(embed=pf.world_records())
        elif msg[1].lower() == "top":
            await message.channel.send(embed=pf.top_x())
        else:
            await message.channel.send(embed=pf.unknown_command(msg[1]))

keep_alive.keep_alive()
client.run(token)

