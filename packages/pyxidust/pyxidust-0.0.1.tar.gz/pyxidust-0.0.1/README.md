# pyxidust

Future general-purpose library.

## Instructions

1. Install:

'''
pip install pyxidust
'''

2. Rename a batch of photos:

'''python
from pyxidust.utils import file_rename

# create a Serials.txt in the directory with one-line of text representing
# the base filemame for the first photo to be renamed (ex. '20220001')
file_rename('/home/photos', '.JPG', 'Serials.txt')
