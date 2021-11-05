import discord
import searchfunctions as sf

def embed_picture(message):
    """ For a given message, make a discord embed with the specified person's
        image (or bufy)
    """

    wcaid = message[2].upper()
    if wcaid != "BUFY":
        imagelink = sf.getimagelink(message)
        name = sf.getname(wcaid)
    else:
        imagelink = """https://cdn.discordapp.com/attachments/714687172418207814/905994981049770014/buffy.png"""
        name = "Bufy"
        wcaid = "1427BUFY01"

    embed = discord.Embed(title=f"{name} ({wcaid})")

    if imagelink != "":
        embed.set_image(url=imagelink)
    else:
        embed.set_image(url="""https://www.worldcubeassociation.org/assets/missing_avatar_thumb-12654dd6f1aa6d458e80d02d6eed8b1fbea050a04beeb88047cb805a4bfe8ee0.png""")

    return(embed)
