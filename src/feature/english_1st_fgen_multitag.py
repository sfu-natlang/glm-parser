import os
def __bootstrap__():
   global __bootstrap__, __loader__, __file__
   import sys, pkg_resources, imp
   __file__ = pkg_resources.resource_filename(__name__,'english_1st_fgen_multitag.so')
   __loader__ = None; del __bootstrap__, __loader__
   imp.load_dynamic(__name__,__file__)

os.environ['PYTHON_EGG_CACHE'] = '~/'
__bootstrap__()
