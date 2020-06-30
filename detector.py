# File to init the program

# Imports python libraries
import sys
import argparse

# Imports local libraries
from bin.Init import Init


# Main function
def main(argv):
  # Parse the parameters
  parser = argparse.ArgumentParser(description='Network Steganography Detector based on OpenAI.')
  parser.add_argument('--verbosity',
                      help='1 - ERROR, 2 - WARNING, 3 - INFO, 4 - INFO MACHINE LEARNING, 10 - DEBUG',
                      default=0, type=int)
  group = parser.add_mutually_exclusive_group(required=True)
  group.add_argument('-d', '--daemon',
                     help='start as a daemon over the configure interface in the settings file',
                     action='store_true')
  group.add_argument('-p', '--pcapfile',
                     help='analyze a PCAP file specifying the traffic type [filename [covert|overt]]',
                     nargs='*', default=[None, None], type=str)
  group.add_argument('-t', '--training',
                     help='train the ML algorithm', action='store_true')
  args = parser.parse_args()

  if args.pcapfile and len(args.pcapfile) > 2:
    print('PARSER ERROR: maximum 2 PCAP parametres: [filename [covert|overt]]')
    exit()
  elif args.pcapfile[0] and len(args.pcapfile) == 2 and \
    args.pcapfile[1] != 'covert' and args.pcapfile[1] != 'overt':
    print('PARSER ERROR: Traffic type should be \'covert\' or \'overt\' or nothing at all')
    exit()
  if (args.verbosity < 0 or args.verbosity > 4) and args.verbosity != 10:
    print('PARSER ERROR: verbosity should be 1 - ERROR, 2 - WARNING, 3 - INFO, 4 - INFO MACHINE LEARNING, 10 - DEBUG')
    exit()

  # Call the init function
  main_app = Init(args.daemon, args.training, args.pcapfile, args.verbosity)
  main_app.Init_startup(args.pcapfile, args.training)
  main_app.Init_main_processing(args.daemon, args.training, args.pcapfile)


# Init
if __name__ == '__main__':
  main(sys.argv[1:])
