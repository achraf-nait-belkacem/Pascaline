import signal
from text import *

def sigint_handler(sig, frame):
    print(QUIT_SIGINT_MSG)
    exit(128 + sig)