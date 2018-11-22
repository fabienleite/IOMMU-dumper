#!/usr/bin/env python3


class Device:
    """
    The device representation
    """

    def __init__(self, device_id, addr, length):
        """
        The Device object constructor

        Attributes:
            - device_id : An integer
            - addr : An integer
            - length : An integer
        """
        self._id = device_id
        self._addr = addr
        self._length = length

    def get_id(self):
        """
        Return the device ID

        Output:
            An integer
        """
        return self._id

    def get_addr(self):
        """
        Return the device start address

        Output:
            An integer
        """
        return self._addr

    def get_length(self):
        """
        Return the device allocated memory length

        Output:
            An integer
        """
        return self._length


class State:
    """
    The state of the memory allocation by IOMMU at a give moment
    """

    def __init__(self, initial_timestamp, device_lst):
        """
        The State object constructor

        Attributes:
            - initial_timestamp : An integer
            - device_lst : A list of Device objects
        """
        self._initial_timestamp = initial_timestamp
        self._devices = device_lst
        self._end_timestamp = None

    def get_initial_timestamp(self):
        """
        Return the state initial timestamp
        
        Output:
            An integer
        """
        return self._initial_timestamp

    def get_device_lst(self):
        """
        Return the list of device mapped at the given state

        Output:
            A list of Device objects
        """
        return self._devices

    def get_end_timestamp(self):
        """
        Return the state end timestamp

        Output:
            An integer
        """
        if self._end_timestamp != None:
            return self._end_timestamp
        else:
            raise Exception(
                "Error : This is the current state, there is no end timestamp"
            )

    def set_end_timestamp(self, end_timestamp):
        """
        Set the state end timestamp

        Attributes:
            - end_timestamp : An integer
        """
        self._end_timestamp = end_timestamp


class Parser:
    """
    A log parser for journalctl & IOMMU logs
    """

    REGEX_LST = [
        r"",
        r"\iommu\: map\: iova.*pa.*size.*",
        r"\iommu\: unmapped\: iova.*size.*",
        r"",
    ]

    def __init__(self, regex_lst):
        """
        The Parser object constructor

        Attributes:
            - regex_lst : A list of Pattern object (compiled REGEX)
        """
        self._regex_lst = regex_lst

    def parse_logs(self, logs):
        """
        Parse your logs to get formated IOMMU logs

        Attributes:
            - logs: A string

        Output:
            - A list of Tuple containing :
                    - An integer (representing Timestamp)
                    - A dictionnary (containing method, address, size, device)
        
                e.g. : [(12456, { "method":"map", "address":0xf8000000, "size":400, "device":0x00000004150b6000 })]
        """
        pass

    def strip_logs(self, logs, regex_lst):
        """
        Select interresting logs for IOMMU context applying the given REGEX list
        
        Attributes:
            - logs: A string
            - regex_lst: A list of Pattern object

        Output:
            - A list of strings
        """
        pass

    def format_logs(self, log_lst):
        """
        Format all the given log lines for IOMMU context

        Attributes:
            - log_lst: A list of strings

        Output:
            - A list of Tuple containing :
                    - An integer (representing Timestamp)
                    - A dictionnary (containing method, address, size, device)
        
                e.g. : [(12456, { "method":"map", "address":0xf8000000, "size":400, "device":0x00000004150b6000 })]
        """
        pass
