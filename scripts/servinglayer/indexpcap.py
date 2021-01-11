#!/usr/bin/env python

import os
import dpkt
import time
import datetime
from dpkt.compat import compat_ord
import asterix
import pandas
import sys
from elasticsearch import Elasticsearch


def mac_addr(address):
    """Convert a MAC address to a readable/printable string
       Args:
           address (str): a MAC address in hex form (e.g. '\x01\x02\x03\x04\x05\x06')
       Returns:
           str: Printable/readable MAC address
    """
    return ':'.join('%02x' % compat_ord(b) for b in address)


def moyenne(liste):
    return somme(liste)/len(liste)


def add_field(container):
    pass


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("need at least 1 file input as argument")
        exit()

    client = Elasticsearch(hosts=["192.168.1.53:50000"])
    document = {}

    ADDR_DIST = ['01:00:5e:50:00:06', '01:00:5e:50:00:22', '01:00:5e:50:00:26', '01:00:5e:50:00:1a', '01:00:5e:50:00:5e', '01:00:5e:50:00:66',
                 '01:00:5e:50:00:52', '01:00:5e:50:00:46', '01:00:5e:50:00:16', '01:00:5e:50:00:12', '01:00:5e:50:01:02', '01:00:5e:50:00:da',
                 '01:00:5e:50:00:0a', '01:00:5e:50:00:2a', '01:00:5e:50:01:42', '01:00:5e:50:00:0e', '01:00:5e:50:00:8e', '01:00:5e:50:00:4a',
                 '01:00:5e:50:00:4e', '01:00:5e:50:00:62', '01:00:5e:50:00:a6', '01:00:5e:50:00:9a', '01:00:5e:50:00:56']

    file_path = sys.argv[1]
    print('start parsing')
    with open(file_path, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)

        for ts, buf in pcap:

            eth = dpkt.ethernet.Ethernet(buf)

            dst = mac_addr(eth.dst)

            if dst in ADDR_DIST[0:1]:
                try:
                    data = eth.data.data.data
                except:
                    data = eth.data.data
                parsed = asterix.parse(data)
                parsed = parsed[0]

                c = parsed['category']

                if c == 48:
                    document["timestamp"] = ts
                    document["date"] =  datetime.datetime.utcfromtimestamp(ts) 
                    document["dest"] = dst
                    try:
                        document["sac"] = parsed['i010']['sac']['val']
                    except:
                        pass
                    try:
                        document["sic"] = parsed['I010']['SIC']['val']
                    except:
                        pass
                    try:
                        document["tod"] = parsed['I140']['ToD']['val']
                    except:
                        pass
                    try:
                        document['tn'] = parsed['I161']['Tn']['val']
                    except:
                        pass
                    try:
                        document['theta'] = parsed['I040']['THETA']['val']
                    except:
                        pass
                    try:
                        document['rho'] = parsed['I040']['RHO']['val']
                    except:
                        pass
                    try:
                        document['fl'] = parsed['I090']['FL']['val']
                    except:
                        pass
                    try:
                        document['cgs'] = parsed['I200']['CGS']['val']
                    except:
                        pass
                    try:
                        document['chgd'] = parsed['I200']['CHdg']['val']
                    except:
                        pass
                    try:
                        document['aa'] = parsed['I220']['ACAddr']['val']
                    except:
                        pass
                    #print(document)
                    response = client.index(
                            index = "category48",
                            doc_type = "test",
                            body = document
                            )
                    if not response["_shards"]["successful"] == 1:
                        print("Index call failed")

        print("end parsing")
