"""
Helps with Saving Files
"""

from pickle import dump, load
from os import walk, getcwd


__author__ = "Anton Alley"
__version__ = "0.0.0"
__copyright__ = "Copyright 2018 Anton Alley all rights reserved"

class OverwriteError(Exception):
    def __init__(self,value):
        self.value = value

    def __str__(self):
        return repr(self.value)

def save(filename, data, warning=False):
    """
    Save some data to the specified .sav file in current directory, or specified path
    """
    if warning:
        input('Warning: will overwite entire file. Press enter to continue')

    filenames = []
    for (_,_,f) in walk(getcwd()):
        filenames.extend(f)
    if f'{filename}.sav' in  filenames:
        raise OverwriteError("Attempted to overwrite a file")
        return None
    
    
    with open(filename+'.sav', 'wb') as f:
        dump(data, f)


def f_open(filename):
    with open(filename+'.sav', 'rb') as f:
        return load(f)
