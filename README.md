# General PCAP Content Sender

This script is intended to UDP-forward the contents of any pcap file to any specified IPv4 Address and Port.
To use, move the desired pcap file into this directory. Run the script and input the file name. 
The following two prompts will request the IP/Port to send to. 

**Note:** The script is currently set to send each payload at a rate of 10Hz.

## Prerequisites

- Python 3
- tkinter
- pyshark

To install the necessary dependencies, run:
```
sudo ./install_dependencies.sh
```

## Usage

1. Move your PCAP file containing J2735 messages to the `logs` directory.
2. Execute the script:
```
cd src
./sender.py
```
3. Follow the prompts
4. To stop script: 
```
<Ctrl-C>
```

