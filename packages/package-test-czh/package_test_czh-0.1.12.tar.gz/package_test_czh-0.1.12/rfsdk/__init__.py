# pyfst - fst client(python)

import os
import sys

rfsdk_root_path = os.path.dirname(__file__)
if rfsdk_root_path not in sys.path:
    sys.path.append(rfsdk_root_path)

pyant_path = os.path.join(rfsdk_root_path, 'pyant')
if pyant_path not in sys.path:
    sys.path.append(pyant_path)

protocol_path = os.path.join(rfsdk_root_path, 'protocol')
if protocol_path not in sys.path:
    sys.path.append(protocol_path)

__version__ = '0.1.0'
