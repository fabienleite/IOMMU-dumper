#!/usr/bin/env python3
import re

def parse_line(line):
    """
    Parse a line to get only wanted datas

    Attributes :
        - A line as String

    Output:
        TODO

    """
    #Regex to verify if it's a known event
    ##Some parenthesis, for the ((? ... )): & (.*) are for grouping, the easily select groups
    r_events = re.compile(r'.*\[[0-9]+\].* ((?:unmap|attach_device_to_domain|detach_device_from_domain|map)):(.*)')
    line=r_events.search(line)
    if line==None:
        raise Exception(
                "Error : unknown event at the line\n%s" % line
        )
    
    event, ev_args = line.groups() #Get the event & the event arguments

    if event=="attach_device_to_domain" or event=="detach_device_from_domain":
        r_args = re.compile(r'.* device=(.*)$')

        device_bdf = r_args.search(ev_args).group(1)
        return {"event_type":event, "bdf":device_bdf}

    elif event=="map":
        r_args = re.compile(r'.* iova=(.*) paddr=(.*) size=(.*)$')
        iova, phys_addr, size = r_args.search(ev_args).groups()
        return {"event_type":event, "iova":iova, "phys_addr":phys_addr, "size":size}

    elif event=="unmap":
        r_args = re.compile(r'.* iova=(.*) size=(.*) unmapped_size=(.*)$')
        iova, size, unmapped_size = r_args.search(ev_args).groups()
        return {"event_type":event, "iova":iova, "size":size, "unmapped_size":unmapped_size}



def parse_file(filename):
    f=[l[:-1] for l in open(filename).readlines()]
    last_attach=None
    for line in f:
        if line[0]!="#":
            out=parse_line(line)
            print(out)
