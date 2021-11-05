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

    msg = message.content.split(" ")

    if message.content.startswith('!wca'):
        if msg[1].lower() == "wr":
            if msg[3].lower() in ["single", "sg"]:
                await message.channel.send(sf.wrsingle(msg))
            elif msg[3].lower() in ["average", "mean", "avg", "mn"]:
                await message.channel.send(sf.wraverage(msg))
        if msg[1].lower() in ["picture", "avatar", "pic"]:
            if msg[2].lower() != "bufy":
                link = sf.getimagelink(msg)
                name = sf.getname(msg[2].upper())
                apostrophe = '\''
                # ugh this is sloppy
                embed = discord.Embed(title=f"{name} ({msg[2].upper()})",
                url=f"{sf.getwcaprofile(msg)}",
                description=f"""{name}{f'{chr(39)}''s' if name[-1] != 's' else 
                f'{chr(39)}'} WCA Profile""")
                if link != None:
                    embed.set_image(url=link)
                await message.channel.send(embed=embed)
            else:
                # Obligatory bufy command
                embed = discord.Embed(title="bufy")
                embed.set_image(url="""https://cdn.discordapp.com/attachments/
                714687172418207814/905994981049770014/buffy.png""")
                await message.channel.send(embed=embed)


keep_alive.keep_alive()
client.run(token)