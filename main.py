import discord

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
        if msg[1] == "wr":
            if msg[2] == "single":
                await message.channel.send("15.27")
            if msg[2] == "mean":
                await message.channel.send("18.18")

client.run(token)

