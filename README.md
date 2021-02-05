# NSD
Network Steganography Detector is a project to detect covert channels on network traffic. It's based on a Random Forest Classifier and uses the PPD technic to extract the features.

The actual version it's only able to detect a specific type of covert timing channel on RTP traffic. In particular, the communication protocol must use two different kind of PDU to send video and audio and the covert channel must modify the PDU's order to transmit the hidden message.

NSD relies on mongodb to store the network traffic and scikit-learn library to develop the machine learning algorithm.

More information (spanish and catalan): http://openaccess.uoc.edu/webapps/o2/handle/10609/118047

# What's new

- v0.92
  * Thread library in network processing
  * First version of traffic state machine workflow


# Installation
pip install -r requirements.txt

# Configuration
There are two files in conf directory:
- settings.py: database, processes, logging, network and machine learning parameters.
- variables.py: global variables (should not be modified).

# Execution
There are three execution modes:
- Daemon: listens in on the interface specified in the settings.py file looking for covert channels. Should be executed with permissions.
- Pcap-file: insert new traffic in the database. Must be specified if the traffic contains a coverth channel or not.
- Training: get the traffic from database that has not been analysed and trains the algorithm.

$ python3 NSD.py (--verbosity [1|2|3|4|10]) [-d|--daemon|-p <pcap_file> [covert|overt]|--pcapfile <pcap_file> [covert|overt]|-t|--training]


