
from urllib import urlopen
from datetime import datetime, timedelta
import sys
from Article import *

if len(sys.argv)>1 :
    try:
        MINLENGTH = int(sys.argv[1])
    except:
        pass

    
