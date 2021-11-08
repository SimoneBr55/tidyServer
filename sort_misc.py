# sort_misc.py
# Version 3.0
import os, sys
#import magic
#import hashlib

#from PIL import Image, ExifTags
#import ffmpeg
import lib.hash as hash_ut ##prevent same name as variable
import lib.media_utilities as media
from lib.write_file import quick_write
# Import environment variables
from decouple import config

# all code required to start preprocessing images.
'''still unused functions
def clean_start(full_path):
    #if filename.startswith("."):
    # Step 1. Remove unwanted temp files
    print(magic.from_file(full_path))
    # Step 2. Get identical images
    print(full_path)


def list_duplicates_of2(seq,item):
    start_at = -1
    locs = []
    while True:
        try:
            loc = seq.index(item,start_at+1)
        except ValueError:
            break
        else:
            locs.append(loc)
            start_at = loc
    return locs

from collections import defaultdict
def list_duplicates_of(seq):
    tally = defaultdict(list)
    for i,item in enumerate(seq):
        tally[item].append(i)
    return ((key,locs) for key,locs in tally.items()
                            if len(locs)>1)
'''

'''
def hashcheck(vid_files, vid_files_names, im_files, im_files_names):
    for video, video_name in zip(vid_files, vid_files_names):
        hash_vid.append(get_hash(video))
        hash_vid_names.append(video)
    for hash, hash_name in zip(list_duplicates_of(hash_vid), hash_vid_names):
        print(hash, hash_name)
    for image, image_name in zip(im_files, im_files_names):
        hash_img.append(get_hash(image))
        hash_img_names.append(image)
    for hash, hash_name in zip(list_duplicates_of(hash_img), hash_img_names):
        print(hash, hash_name)
    #WHAT SHOULD IT RETURN???
'''

im_extensions = (".jpeg", ".jpg", ".png", ".gif")
vid_extensions = (".mp4", ".mov", ".avi", ".MP4")

path = config('saved_path')
storage_path = config('misc_path')
no_date = config('no_date_path')
im_files = []
im_files_names = []
vid_files = []
vid_files_names = []
noname = 0

for root, d_names, f_names in os.walk(path):
    for f in f_names:
        if f.endswith(im_extensions):
            im_files.append(os.path.join(root,f))
            im_files_names.append(f)
        elif f.endswith(vid_extensions):
            vid_files.append(os.path.join(root,f))
            vid_files_names.append(f)


for image, name in zip(im_files, im_files_names):
    #print(image)
    exif = media.extract(image)
    if exif == None:
        try:
            year, month, day = media.no_names(name)
            #new_path = storage_path+"/"+year+"/"+month+"/"+day+"/"+name
            new_path = storage_path+"/"+year+"/"+month+"/"+name
        except:
            new_path = no_date+"/"+name
            noname += 1
        print(image, new_path)
        os.rename(image, new_path)
        continue
    field = media.get_field(exif,"DateTimeOriginal")
    if field == None:
        try:
            year, month, day = media.no_names(name)
            #new_path = storage_path+"/"+year+"/"+month+"/"+day+"/"+name
            new_path = storage_path+"/"+year+"/"+month+"/"+name
        except:
            new_path = no_date+"/"+name
            noname += 1
        print(image, new_path)
        os.rename(image, new_path)
	new_file.append(new_path)
        continue
    else:
        year = field[0]+field[1]+field[2]+field[3]
        month = field[5]+field[6]
        day = field[8]+field[9]
        #new_path = storage_path+"/"+year+"/"+month+"/"+day+"/"+name
        new_path = storage_path+"/"+year+"/"+month+"/"+name
    print(image, new_path)
    new_file.append(new_path)
    os.rename(image, new_path)

for video, name in zip(vid_files, vid_files_names):
    try:
        year, month, day = media.extract_vid(video)
        #new_path = storage_path+"/"+year+"/"+month+"/"+day+"/"+name
        new_path = storage_path+"/"+year+"/"+month+"/"+name
        print(video, new_path)
        new_file.append(new_path)
        os.rename(video, new_path)
    except:
        #print("No Date")
        try:
            year, month, day = media.no_names(name)
            #new_path = storage_path+"/"+year+"/"+month+"/"+day+"/"+name
            new_path = storage_path+"/"+year+"/"+month+"/"+name
        except:
            noname += 1
            new_path = no_date+"/"+name
        print(video, new_path)
        new_file.append(new_path)
        os.rename(video, new_path)
print(noname)

for n_f in new_file:
    try:
        quick_write("/tmp/new_files", n_f)
    except:
        echo "ERROR WRITING /tmp/new_files"
