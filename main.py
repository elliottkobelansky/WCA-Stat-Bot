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
        if msg[1].lower() == "wr":
            if msg[3].lower() in ["single", "sg"]:
                await message.channel.send(embed=ef.embed_result(msg))
            elif msg[3].lower() in ["average", "mean", "avg", "mn"]:
                await message.channel.send(sf.wraverage(msg))
        if msg[1].lower() in ["picture", "avatar", "pic"]:
            await message.channel.send(embed=ef.embed_picture(msg[2]))
        if msg[1].lower() == "ben":
            await message.channel.send(embed=ef.embed_result(msg))


keep_alive.keep_alive()
client.run(token)