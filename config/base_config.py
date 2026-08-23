import os
import sys

DIR_PATH = os.path.dirname(os.path.dirname(__file__))
sys.path.append(DIR_PATH)

File_PATH={
    'extract':os.path.join(DIR_PATH,'extract.yaml'),
    'ini':os.path.join(DIR_PATH,'config','config.ini'),
}

