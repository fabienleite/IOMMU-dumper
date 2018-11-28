#!/usr/bin/env python3
import re
import os


def parse_line(line):
    """
    Parse a line to get only wanted datas

    Attributes :
        - A line as String

    Output:
        - A dictionary. Dictionary can have 3 formats :
            MAP EVENT           {event_type, iova, phys_addr, size}
            UNMAP EVENT         {event_type, iova, size, unmapped_size}
            ATTACH/DETACH EVENT {event_type, device_bdf}

    """
    # Regex to verify if it's a known event
    ##Some parenthesis, for the ((? ... )): & (.*) are for grouping, the easily select groups
    r_events = re.compile(
        r".*\[[0-9]+\].* ((?:unmap|attach_device_to_domain|detach_device_from_domain|map)):(.*)"
    )
    p_line = r_events.search(line)
    if p_line == None:
        return None

    event, ev_args = p_line.groups()  # Get the event & the event arguments

    if event == "attach_device_to_domain" or event == "detach_device_from_domain":
        r_args = re.compile(r".* device=(.*)$")

        device_bdf = ":".join(
            r_args.search(ev_args).group(1).split(":")[1:]
        )  # Remove PCI domain to BDF
        return {"event_type": event, "device_bdf": device_bdf}

    elif event == "map":
        r_args = re.compile(r".* iova=(.*) paddr=(.*) size=(.*)$")
        iova, phys_addr, size = r_args.search(ev_args).groups()
        return {"event_type": event, "iova": iova, "phys_addr": phys_addr, "size": size}

    elif event == "unmap":
        r_args = re.compile(r".* iova=(.*) size=(.*) unmapped_size=(.*)$")
        iova, size, unmapped_size = r_args.search(ev_args).groups()
        return {
            "event_type": event,
            "iova": iova,
            "size": size,
            "unmapped_size": unmapped_size,
        }


def parse_tracefile(filename="/sys/kernel/debug/tracing/trace"):
    """
    Parses a trace file to get IOMMU events and their arguments.
    Add device_bdf & device_name to MAP EVENT
    Add device_name to ATTACH/DETACH EVENT

    Attributes:
        - A file name as String. 
            By default, the /sys/kernel/debug/tracing/trace file

    Output:
        - A list of Dictionary. Dictionary can have 3 formats :
            MAP EVENT           {event_type, device_bdf, device_name, iova, phys_addr, size}
            UNMAP EVENT         {event_type, iova, size, unmapped_size}
            ATTACH/DETACH EVENT {event_type, device_bdf, device_name}

    """
    try:
        f = open(filename)
        f_content = [l[:-1] for l in f.readlines()]
        f.close()
    except (IOError, FileExistsError) as e:
        raise e

    last_attach = None

    parsed_traces = []

    for line in f_content:
        if line[0] != "#":
            parsed_line = parse_line(line)
            if parsed_line == None:
                continue

            if parsed_line["event_type"] == "attach_device_to_domain":
                lspci_output = os.popen(
                    "lspci -s %s" % parsed_line["device_bdf"]
                ).read()
                device_name = lspci_output[
                    len(parsed_line["device_bdf"]) : -1
                ]  # Remove BDF & newline char
                parsed_line["device_name"] = device_name

                last_attach = (parsed_line["device_bdf"], device_name)
            elif parsed_line["event_type"] == "map":
                try:
                    assert last_attach != None
                    parsed_line["device_bdf"] = last_attach[0]
                    parsed_line["device_name"] = last_attach[1]
                except AssertionError:
                    raise Exception(
                        'Error : "map" event can\'t appear before "attach_device_to_domain" event'
                    )

            elif parsed_line["event_type"] == "detach_device_from_domain":
                lspci_output = os.popen(
                    "lspci -s %s" % parsed_line["device_bdf"]
                ).read()
                device_name = lspci_output[
                    len(parsed_line["device_bdf"]) : -1
                ]  # Remove BDF & newline char
                parsed_line["device_name"] = device_name

            parsed_traces.append(parsed_line)

    return parsed_traces


if __name__ == "__main__":
    # Depends on the Linux Architecture
    parsing = parse_tracefile()
    print(parsing)
