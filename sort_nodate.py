# Experimental script to sort videos and pictures seamingly with no info on date...

import lib.media_utilities as media
import os

from decouple import config

path = config('no_date_path') #here pictures tree should be already flat, but anyway let's leave it open
storage_path = config('misc_path')
for root, d_names, f_names in os.walk(path):
    for f in f_names:
        try:
            year, month, day = media.no_names(f)
            new_path = storage_path+"/"+year+"/"+month+"/"+f
            file = os.path.join(root,f)
            print(f,new_path)
            os.rename(file, new_path)
            continue
        except Exception as e:
            print(e)
            continue
