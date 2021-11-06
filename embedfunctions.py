import discord
import searchfunctions as sf


def embed_result(message):
    """ Prints out result that was requested by the user
    """
    if message[1].lower() == "wr":
        info = sf.get_wr_result(message)
    elif message[1].lower() == "nr":
        info = sf.get_nr_result(message)

    if info['rank'] == 1: info['rank'] = "" 
    # Gets image for a given WCAID
    link = sf.getimagelink(info["wcaid"])
    
    embed = discord.Embed(title=f"{info['name']} ({info['wcaid']})")
    embed.set_thumbnail(url=link)
    embed.add_field(name=f"{info['country']}{info['ranktype']}{info['rank']} {info['solvetype']}:", 
                    value=f"{info['time']}")
    return(embed)


def embed_picture(wcaid):
    """ For a given message, make a discord embed with the specified person's
        image
    """

    wcaid = wcaid.upper()
    # Bufy Easter egg
    if wcaid != "BUFY":
        imagelink = sf.getimagelink(wcaid)
        name = sf.getname(wcaid)
    else:
        imagelink = f"""https://cdn.discordapp.com/attachments/714687172418207814/905994981049770014/buffy.png"""
        name = "Bufy"
        wcaid = "1427BUFY01"

    embed = discord.Embed(title=f"{name} ({wcaid})")

    if imagelink != "":
        embed.set_image(url=imagelink)
    else:
        # Some people dont even have the default image for some reason so this
        # just sets it to the default one
        embed.set_image(url="""https://www.worldcubeassociation.org/assets/missing_avatar_thumb-12654dd6f1aa6d458e80d02d6eed8b1fbea050a04beeb88047cb805a4bfe8ee0.png""")

    return(embed)
