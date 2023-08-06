import os
from . import policyapp

def get_template_dirs():
    """
    Template search paths..
    """
    thisdir = os.path.dirname(os.path.abspath(__file__))
    return [
        os.path.join(thisdir, 'policyapp', 'templates')
    ]
