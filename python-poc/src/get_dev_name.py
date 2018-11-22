#!/usr/bin/env python

import os


def get_dev_name(dev):
    """
    Get a device full name from its Bus Device Function.

    Attributes:
        - Device's BDF : A string

    Output:
        - A string
    """
    lspci = os.popen("lspci -s " + dev).read()
    dev_name = " ".join(lspci.split(" ")[1:])[
        :-1
    ]  # Get the device name without BDF & the newline (\n) at the end
    return dev_name


def get_devs():
    """
    Get the list a enabled devices.

    Output:
        - A dictionnary with :
                - Device's BDF as key
                - Device's name as item
    """
    enabling_list = os.popen("dmesg | grep 'enabling device'").read().split("\n")[:-1]
    devs = {}
    for line in enabling_list:
        bdf = line.split(" ")[3][:-1]  # Get the BDF without the ":" at the end
        if bdf not in devs.keys():
            name = get_dev_name(bdf)
            devs[bdf] = name
    return devs
