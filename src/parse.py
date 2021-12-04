# Parses messages entered by the user and returns embeds. 
# For main.py. 

import embed as ef
import search as sf
import wcautils as wu
import re



def best_from_rank(msg):
    # Message comes in in the form ["wr", "5", "s", "333bf" ]
    # Or, (Continental) ["ocr", "3", "a", "333"]
    # Or, (National) ["nr", "5", "s", "444bf", "canada"]
    
    errors = []
    
    if wu.is_valid_ranktype(msg[0]):
        ranktype = msg[0].upper()
        
        if ranktype == "WR":
            region = "world"
        elif ranktype == "NR":
            region = "country"
        else:
            region = wu.get_CR_region(ranktype)
            
        
    else:
        errors.append("Please enter a valid ranktype (nr, wr, nar, ...)")
    
    if re.search("^\d+$", msg[1]):
        rank = msg[1]
    else:
        errors.append("Please enter a valid rank as an integer")
                      
    if wu.single_or_avg(msg[2]):
        solvetype = wu.single_or_avg(msg[2])
    else:
        errors.append("Please enter a valid solvetype (single or average)")
    
    if len(msg) > 4:
        try: 
            region = wu.get_country(" ".join(msg[3:-1]))
        except:
            errors.append("Please enter a valid country")  
     
    try: 
        eventid = wu.get_eventid(msg[-1]) 
    except:
        errors.append("Please enter a valid event")       

    if errors:
        return ef.embed_errors("\n".join(errors))
    
    else:
        return ef.embed_result(sf.ResultRequest(solvetype, eventid, region, rank), ranktype)
        
        
def profile(msg):
    ''' Returns an embed for a given wca profile based on request. 
    ''' 
    
    if wu.is_wca_id_form(msg[0]):
        wcaid = uf.get_wcaid(msg[0])
        if wcaid:
            return ef.embed_profile(sf.WcaPerson(wcaid))
        else:
            return ef.embed_errors("Invalid WCA ID.")
    
    else: 
        wcaid = wu.get_wcaid_from_name(msg)
        if wcaid:
            return ef.embed_profile(sf.WcaPerson(wcaid))
        else:
            return ef.embed_errors("No WCA profile corresponds to the name that was enterred.")
    
        


