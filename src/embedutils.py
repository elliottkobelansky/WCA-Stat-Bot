# The utilities needed for embed.py
# This consists mostly of functions to format text to be embed-ready

import wcautils as wu


def format_profile_results(results):
    ''' Takes in results in form:
        {Single: {event: [best, wr, cr, nr], ...}, Average: {...}}
        Outputs in block style discord format.
    '''
    
    values = [["Event", "Single", "Average"]]
    
    for event, result in results["Single"].items():
        eventname = wu.get_event_name(event)
        if eventname:
            s = wu.Result(event, result[0], "Single")
            try:
                a = wu.Result(event, results["Average"][event][0], "Average")
                values.append([
                    eventname,
                    s.best,
                    a.best      
                ])
            except:
                values.append([
                    eventname,
                    s.best,
                    "-"
                ])
    
    values.sort(key=lambda x: wu.sort_events(x[0]))
    
    listsize = range(len(values[0]))
    widths = [max([len(row[c]) for row in values]) for c in listsize]
    
    formatted = []
    for row in values:
        line = ''
        for i in listsize:
            s = row[i]
            line = line + s + ' ' * (widths[i] - len(s) + 1) + '  '
        formatted.append(line)
        
    lineseparator = "-" * (sum(widths) + 3 * (len(widths) - 1) + 2)
    formatted.insert(0, "```")
    formatted.insert(2, lineseparator)
    formatted.append("```")
    formatted = "\n".join(formatted)
    
    return formatted