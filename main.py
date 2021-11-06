import discord
import searchfunctions as sf
import embedfunctions as ef
import keep_alive

with open('token.txt') as f:
    token = f.read()


client = discord.Client()

@client.event
async def on_ready():
    print('We have loggen in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content.split(" ")

    if message.content.startswith('!wca'):
        if msg[1].lower() in  ["wr", "nr"]:
            await message.channel.send(embed=ef.embed_result(msg))
        if msg[1].lower() in ["picture", "avatar", "pic"]:
            await message.channel.send(embed=ef.embed_picture(msg[2]))

keep_alive.keep_alive()
client.run(token)