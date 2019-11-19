# File to init the program

# Imports python libraries
import sys
import getopt

# Imports NSD libraries
from bin.NSD_Main import NSD_Main

def main(argv):
    daemon = False
    pcap_file = None
    try:
        opts, args = getopt.getopt(argv, "hd:p:", ["pcap_file"])
    except getopt.GetoptError:
        print('NSD.py [-d|-p <pcap_file>]')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('NSD.py [-d|-p <pcap_file>]')
            sys.exit()
        elif opt in ('-p', '--pcap_file'):
            pcap_file = argv
        elif opt == '-d':
            daemon = True

    NSD_Main(daemon, pcap_file)

# Init
if __name__ == '__main__':
    main(sys.argv[1:])
