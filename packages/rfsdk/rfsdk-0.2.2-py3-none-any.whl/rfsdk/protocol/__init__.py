import os
import sys

protocol_root_path = os.path.dirname(__file__)

if protocol_root_path not in sys.path:
    sys.path.append(protocol_root_path)
