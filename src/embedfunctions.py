import discord
import searchfunctions as sf
import re


def create_person_embed_header(Person):
    embed = discord.Embed(title=f"{Person.name} - {Person.get_country()}  {Person.get_emoji()}",
                          url=Person.get_wca_link(), color=discord.Color.blue())
    embed.set_thumbnail(url=Person.get_image_link())
    return(embed)


def embed_result(message):
    """ Prints out result that was requested by the user
    """

    info = sf.getresult(message)
    wcaid = info['wcaid']
    Person = sf.WcaPerson(wcaid)
    time = sf.ResultTime(info['best'], info['eventid'],
                         info['solvetype']).ftime

    # Removes redudant 1 in front of record (WR1 => WR)
    if info['rank'] == "1":
        info['rank'] = ""

    embed = create_person_embed_header(Person)
    embed.add_field(name=f"{info['event']} {info['ranktype']}{info['rank']} {info['solvetype']}",
                    value=f"{time}")

    if info['solvetype'] == "Average":
        avgtimes = sf.getavgtimes(info)
        embed.set_footer(text=avgtimes)

    return(embed)


def embed_profile(message):

    if re.search("\d\d\d\d\D\D\D\D\d\d", message[0]) != None:
        wcaid = message[0].upper()
    else:
        wcaid = sf.get_person_wca_id(message)

    Person = sf.WcaPerson(wcaid)
    single_results = Person.parse_single_results()
    average_results = Person.parse_average_results()
    embed = create_person_embed_header(Person)

    events_s_a = [["Event", "Single", "Average"]]

    for result in single_results:
        try:
            events_s_a.append(
                [result,
                 single_results[result][0],
                 average_results[result][0],
                 ])
        except:
            events_s_a.append(
                [result,
                 single_results[result][0],
                 "-"
                 ])

    events_s_a.sort(key=lambda x: sf.sort_events(x[0]))

    # ripped from berkeley exam (thanks anto)
    listsize = range(len(events_s_a[0]))
    widths = [max([len(row[c]) for row in events_s_a]) for c in listsize]
    formatted = []
    for row in events_s_a:
        line = ''
        for i in listsize:
            s = row[i]
            line = line + s + ' ' * (widths[i] - len(s) + 1) + '  '
        formatted.append(line)

    lineseparator = "-" * (sum(widths) + 3 * (len(widths) - 1) + 2)
    formatted.insert(0, f"```")
    formatted.insert(2, lineseparator)
    formatted.append("```")
    formatted = "\n".join(formatted)
    
    competitioncount = Person.get_competition_count()

    embed.add_field(name="Results", value=formatted, inline=True)
    embed.set_footer(text=f"Competitions: {competitioncount}")

    return(embed)


def world_records():
    
    embed = discord.Embed(title="Current World Records")
    wrs = sf.getwrs()
    wrs.sort(key=lambda x: sf.sort_events(x[1]))
    it = iter(wrs)
    for i in it:
        a = i
        try:
            b = next(it)
        except:
            b = None
        if b:
            embed.add_field(name=f"{a[1]}:", value=f"Single: {a[0]}, {a[2]} \nAverage: {b[0]}, {b[2]}", inline=False)
        else:
            embed.add_field(name=f"{a[1]}:", value=f"{a[0]}, {a[2]}")
        
    return(embed)

def top_x(msg):
    x = msg[0]
    solvetype = msg[1] # Single or average
    region = msg[2]
    event = msg[3]
    
    if x > 20 or x < 1:
        embed = embed.discord.Embed(
            name="Error", value="Please enter a value between 1 and 25"
            )
        return(embed)

    results = sf.get_top_x(x, solvetype, region, event)
    
    pass

def embed_help():
    # TODO, obviously
    embed.discord.Embed(name="Help")
    pass
