import os
import assets
accinfo = os.path.exists('accinfo.ini')
if(accinfo == True):
    from assets import main
else:
    from assets import setup