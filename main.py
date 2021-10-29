import discord
import searchfunctions


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
        # Always be case insensitive
        if msg[1].lower() == "wr":
            # Tried to throw in some shorthands
            if msg[3].lower() in ["single", "sg"]:
                # Look at searchfunctions.py to see what this does
                await message.channel.send(searchfunctions.wrsingle(msg))
            elif msg[3].lower() in ["average", "mean", "avg", "mn"]:
                await message.channel.send(searchfunctions.wraverage(msg))


client.run(token)