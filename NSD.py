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
    group.add_argument('-t', '--training', help='train the AI algorithm', action='store_true')
    group.add_argument('-a', '--analyze', help='just analyze database packets. In daemon mode is not required.', action='store_true')
    args = parser.parse_args()

    # Call the NSD init function
    main_app = NSD_Init(args.daemon, args.training, args.pcapfile, args.analyze)
    main_app.NSD_Init_startup(args.pcapfile, args.training, args.analyze)

    if args.daemon:
        main_app.NSD_Init_daemon()
    elif args.pcapfile:
        main_app.NSD_Init_analyze_pcap()

    return main_app.NSD_exit()

# Init
if __name__ == '__main__':
    main(sys.argv[1:])
