import discord
import searchfunctions as sf
import re




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
