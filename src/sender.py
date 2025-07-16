#!/usr/bin/env python3
"""Send/replay raw PCAP using UDP"""
import os, sys, socket, pyshark
import datetime
import argparse
from binascii import unhexlify
from time import sleep
from tkinter import Tk, filedialog

def browse_file():
    """Open file dialog and return the selected file path"""
    root = Tk()
    root.withdraw()
    srcDir = os.path.dirname(os.path.abspath(__file__))
    logDir = os.path.join(srcDir, '../logs')
    filename = filedialog.askopenfilename(initialdir=logDir,
                                          title = "Select a File",
                                          filetypes=[("PCAP Files", "*.pcap")])
    return filename

def extract_packets(pcap_file):
    """Extract packets from the PCAP file and return a list of packet data."""
    capture = pyshark.FileCapture(pcap_file, display_filter='udp')
    packets = []
    
    for packet in capture:
        try:
            packets.append(packet.data.data)
        except AttributeError:
            continue
    
    return packets


def main():
    parser = argparse.ArgumentParser(description='Script to parse and forward J2735 V2X Messages as they are received over UDP')
    parser.add_argument('--udp_ip', help='IP address to receive UDP data.', type=str, default="127.0.0.1") 
    parser.add_argument('--udp_port', help='Port to receive UDP data.', type=int, default=5398)
    args = parser.parse_args()

    sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    file = browse_file()
    if not file:
        print("No file selected. Exiting.")
        sys.exit(1)
    packets = extract_packets(file)
    if not packets:
        print("No UDP packets found in the selected file. Exiting.")
        sys.exit(1)

    print('Sending.\n<Ctrl+c> to exit\n')
    print('Time start: ', datetime.datetime.now())
    # while(1):
    for line in packets:
        data = line.strip('\n')
        # print(data)                 # uncomment to view data to be sent 
        
        unhexed = unhexlify(data)
        sk.sendto(unhexed,(args.udp_ip, args.udp_port))
        sleep(0.1) # 0.1 for BSM or SPAT or a pre-recorded message with multiple message types, 1 for ONLY Map

    print('Time end: ', datetime.datetime.now())
    sys.exit(0)

if __name__=="__main__":
    main()
