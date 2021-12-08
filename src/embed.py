import discord
import search as sf
import wcautils as wu
import embedutils as eu
import re

def create_person_embed_header(WcaPerson):
    ''' Creates the header of the embed, given a WcaPerson object.
    '''
    
    embed = discord.Embed(
        title=f"{WcaPerson.name()} - {WcaPerson.country()}  {WcaPerson.emoji()}",
        url=WcaPerson.wca_link(),
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=WcaPerson.image_link())
    
    return embed


def embed_result(ResultRequest, ranktype):
    results = ResultRequest.get_result() 
    if results: 
        wcaid, best, rank = results
        
    else:
        return embed_errors(f"Likely cause: The inputted region ({ResultRequest.region}) does not have result corresponding to your query") 
        
    WcaPerson = sf.WcaPerson(wcaid)
    solvetype = ResultRequest.solvetype
    rank = rank if rank != "1" else ""
    event = wu.get_event_name(ResultRequest.eventid)
    time = wu.Result(event, best, solvetype).best 
    
    
    embed = create_person_embed_header(WcaPerson)
    embed.add_field(
        name=f"{event} {ranktype}{rank} {solvetype}",
        value=f"{time}"
        )
    
    if solvetype == "ben": # Reprogram this function
        avgtimes = wu.get_avg_times(ResultRequest)
        embed.set_footer(text=avgtimes)
        
    return embed
    
    
def embed_profile(WcaPerson):
    results = WcaPerson.results()
    embed = create_person_embed_header(WcaPerson)
    formatted = eu.format_profile_results(results)
    embed.add_field(name="Results", value=formatted)
    # Add Competition count and/or Medal Count
    
    return embed


def embed_records(Region):
    records = Region.get()
    
    pass

def embed_errors(string):
    embed = discord.Embed(title="Error", color=discord.Color.red(), 
                          description=("```\n" + string + "\n\nUse \"!wca help\" for help```"))
    return embed
    
    
        
