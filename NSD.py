# File to init the program

# Imports python libraries
import sys
import argparse

# Imports NSD libraries
from bin.NSD_Init import NSD_Init


# Main function
def main(argv):

    # Parse the parameters
    parser = argparse.ArgumentParser(description='Network Steganography Detector based on OpenAI.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-d', '--daemon', help='start as a daemon over the configure interface in the settings file', action='store_true')
    group.add_argument('-p', '--pcapfile', help='parse and analyze a PCAP file', type=str)
    args = parser.parse_args()

    # Call the NSD init function
    main_app = NSD_Init(args.daemon, args.pcapfile)
    main_app.NSD_Init_startup()

    if args.daemon:
        main_app.NSD_Init_daemon()
    else:
        main_app.NSD_Init_analyze_pcap()

# Init
if __name__ == '__main__':
    main(sys.argv[1:])
