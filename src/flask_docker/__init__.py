import os, sys
import pkgutil
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
__path__ = pkgutil.extend_path(__path__, __name__)