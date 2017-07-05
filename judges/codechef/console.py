'''
The module handles various print functions
'''
from __future__ import print_function
import sys

verbose=True
silent=False
#if both verbose and silent then verbose should dominate

def error(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    
    
def ifverbose(*args, **kwargs):
    if(verbose==True):
        print(*args, file=sys.stdout, **kwargs)
        
def log(*args, **kwargs):
    if(silent==False or verbose==True):
        print(*args, file=sys.stdout, **kwargs)
