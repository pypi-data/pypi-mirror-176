import os
import sys

real_path = os.path.dirname(os.path.abspath(__file__)).replace("\\","/")
sys.path.append(real_path)

__version__ = '1.2.2'

from .matching import dotshow as dotshow
from .matching import colorshow as colorshow
from .matching import loadshow as loadshow

__all__ = [dotshow, loadshow, colorshow]
