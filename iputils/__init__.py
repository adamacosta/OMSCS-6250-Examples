"""Utilities for handling IP addresses.

Exports:

Classes
-------
IP -- A bit representation of an IP address that supports longest prefix
    matching.

CIDRBlock -- Converts an IP address in CIDR notation to a range of valid 
    addresses matching the block.

Functions
---------
ip_parser([string]) -> [IP|CIDRBlock]
    Parses a string in dotted quad format to either an IP object or a 
    CIDRBlock object depending upon the presence of a trailing mask.

Requires:

numpy
bitarray
"""

from iputils import *