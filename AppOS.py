import os
import assets

__version__ = "1.2.6"

accinfo = os.path.exists('accinfo.ini')
if(accinfo == True):
    from assets import main
else:
    from assets import setup