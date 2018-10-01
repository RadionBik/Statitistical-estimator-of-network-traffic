# Statitistical-estimator-of-network-traffic

The program consists of 2 main parts:

- Traffic estimator
- Traffic generator

The estimator takes a pcap file and for all (or specified in addresses_to_check.txt) flows extracts the Payload Length and the Inter-Arrival Time parameters. Afterwards, EM-algorithm is applied to fit a gaussian mixture (up to 5 components) to the parameters and the trained model is saved to a file in the obj/ folder.

E.g.:
    
    ./stat_estimator.py -p traffic_dumps/rtp_711.pcap -f all --plot --save-plot

The generator uses the saved EM-model to generate packets with length and delay drawn from the estimated distributions. The side has to be specified, either 'local' (the estimated side) or 'remote' (remote end).   

E.g.:

local side:
    
    ./packet_transceiver.py -m local -d 172.17.0.3 -o obj/rtp_711_UDP_10_1_3_143_5000_auto_components.pkl -i eth0

remote side:
    
    ./packet_transceiver.py -d 172.17.0.2 -o obj/rtp_711_UDP_10_1_3_143_5000_auto_components.pkl -m remote