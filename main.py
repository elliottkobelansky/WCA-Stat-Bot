import discord
import searchfunctions as sf
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

    msg = message.content.lower()
    msg = msg.split(" ")

    if message.content.startswith('!wca'):
        if msg[1] == "wr":
            if msg[3] in ["single", "sg"]:
                await message.channel.send(sf.wrsingle(msg))
            elif msg[3] in ["average", "mean", "avg", "mn"]:
                await message.channel.send(sf.wraverage(msg))
        if msg[1] == "picture":
            link = sf.getimage(msg)
            embed = discord.Embed(title=f"{sf.getname(msg[1])}")
            embed.set_image(url=sf.getimagelink(msg))
            await message.channel.send(embed=embed)


keep_alive.keep_alive()
client.run(token)