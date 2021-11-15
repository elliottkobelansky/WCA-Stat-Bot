import discord
import searchfunctions as sf

def create_person_embed_header(Person):
    embed = discord.Embed(title=f"{Person.name} - {Person.country}  {Person.emoji}",
                          url=Person.wcalink, color=discord.Color.blue())
    embed.set_thumbnail(url=Person.imagelink)
    return(embed)


def embed_result(message):
    """ Prints out result that was requested by the user
    """
    
    info = sf.getresult(message)
    wcaid = info['wcaid']
    Person = sf.WcaPerson(wcaid)
    time = sf.ResultTime(info['best'], info['eventid']).ftime

    # Removes redudant 1 in front of record (WR1 => WR)
    if info['rank'] == "1": info['rank'] = ""
    
    embed = create_person_embed_header(Person)
    embed.add_field(name=f"{info['event']} {info['ranktype']}{info['rank']} {info['solvetype']}", 
                    value=f"{time}")

    if info['solvetype'] == "Average":
        avgtimes = sf.getavgtimes(info)
        embed.set_footer(text=avgtimes)

    return(embed)


def embed_profile(message):

    wcaid = sf.get_person_wca_id(message)
    Person = sf.WcaPerson(wcaid)
    single_results = Person.parse_single_results()
    average_results = Person.parse_average_results()

    for row in single_results:
        pass
    
    embed = create_person_embed_header(Person)

    events_s_a = []
    
    for result in single_results:
        try:
            events_s_a.append(
                [result, 
                single_results[result][0], 
                average_results[result][0]]
                )
        except:
            events_s_a.append([result, single_results[result][0], "-"])

    
    events_s_a.sort(key=lambda x: sf.sort_events(x[0]))
    events = [x[0] for x in events_s_a]
    singletimes = [x[1] for x in events_s_a]
    averagetimes = [x[2] for x in events_s_a]
    events = "\n".join(events)
    singletimes = "\n".join(singletimes)
    averagetimes = "\n".join(averagetimes)
  

    embed.add_field(name="Event", value=events, inline=True)
    embed.add_field(name="Single", value=singletimes, inline=True)
    embed.add_field(name="Average", value=averagetimes, inline=True)
    #embed.add_field(name="WR", value=wr_a_ranks, inline=True)
    #embed.add_field(name="CR", value=cr_a_ranks, inline=True)
    #embed.add_field(name="NR", value=nr_a_ranks, inline=True)

    return(embed)
    
    
    pass


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


def embed_help():
    # TODO, obviously
    embed.discord.Embed(name="Help")
    pass
