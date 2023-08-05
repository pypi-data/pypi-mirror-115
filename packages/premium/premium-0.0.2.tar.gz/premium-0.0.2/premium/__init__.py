import builtins

import codefast as cf

from premium.preprocess import Pickle
from premium.datasets import Downloader 

builtins.salt = Pickle()
downloader = Downloader()


