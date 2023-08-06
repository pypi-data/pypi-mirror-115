# -*- coding: utf-8 -*-
#
# Copyright (c) 2021~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from typing import *
import os
import sys
import ipaddress

def ip4to6(ip: str) -> Dict[str, str]:
    '''
    convert ipv4 to ipv6.
    '''
    ipv4 = ipaddress.IPv4Address(ip)
    ipv6 = ipaddress.IPv6Address('::ffff:' + ipv4.compressed)
    return {
        'default': '::ffff:' + ipv4.compressed,
        'exploded': ipv6.exploded,
        'compressed': ipv6.compressed,
    }

def main(argv=None):
    if argv is None:
        argv = sys.argv

    if not len(argv) == 2:
        raise SystemExit('usage: ip4to6.py {IP}')

    for key, value in ip4to6(argv[1]).items():
        print(f'{key}:\n   {value}')

if __name__ == '__main__':
    main()

__all__ = ['ip4to6']
