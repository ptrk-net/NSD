# File to define the global variables.

# --------------------------
#   SHOULD NOT BE MODIFIED
# --------------------------

# FLOW STATUS
FLOW_UPDATING = 0
FLOW_STANDBY = 1
FLOW_FINISHED = 2
FLOW_ARCHIVED = 3

# FLOW ML PROCESSING STATUS
FLOW_ML_TRAINING = 0
FLOW_ML_FINISHED = 1
FLOW_ML_NOT_STARTED = 2
FLOW_ML_PT1_WORKING = 3
FLOW_ML_PT1_WAITING = 4
FLOW_ML_PT1_FINISHED = 5
FLOW_ML_PS12_WORKING = 6
FLOW_ML_PS12_WAITING = 7
FLOW_ML_PS12_FINISHED = 8

# FLOW ML RESULT
FLOW_ML_POSITIVE = 0
FLOW_ML_NEGATIVE = 1
FLOW_ML_SUSPECT = 2
FLOW_ML_TRAINED = 3

# TYPE COVERT CHANNEL
CC_PT1 = 0
CC_PT2 = 1
CC_PT11 = 11

# LOG LEVEL
NONE = 0
ERROR = 1
WARNING = 2
INFO = 3
INFO_ML = 4
DEBUG = 10
