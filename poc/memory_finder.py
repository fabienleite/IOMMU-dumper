#!/usr/bin/env python
import os
import re

def find_memory_addr(dev_ID):
    """
    Find a Device's memory memory address from its ID.

    Input :
        - dev_ID : The Device's ID as a String

    Output :
        - A list of BAR
    """
    lspci = os.popen("lspci -vs %s" % dev_ID).read()
    
    r_memory = re.compile(r"Memory at (\w+) \(")
    all_base_addr = r_memory.findall(x)

    return all_base_addr


if __name__=="__main__":
    print(find_memory_addr("00:00.0"))
