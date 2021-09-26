# sort_misc.py
# Version 2.0
import os, sys
import magic
import hashlib

from PIL import Image, ExifTags
import ffmpeg

# Import environment variables
from decouple import config

# all code required to start preprocessing images.
def get_hash(full_path):
    return hash_bytestr_iter(file_as_blockiter(open(full_path, 'rb')), hashlib.md5())

def clean_start(full_path):
    #if filename.startswith("."):
    # Step 1. Remove unwanted temp files
    print(magic.from_file(full_path))
    # Step 2. Get identical images
    print(full_path)



def hash_bytestr_iter(bytesiter, hasher, ashexstr=False):
    for block in bytesiter:
        hasher.update(block)
    return hasher.hexdigest() if ashexstr else hasher.digest()

def file_as_blockiter(afile, blocksize=65536):
    with afile:
        block = afile.read(blocksize)
        while len(block) > 0:
            yield block
            block = afile.read(blocksize)


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


def extract(image):
    try:
        img = Image.open(image)
        exif = img._getexif()
        return exif
    except:
        return None

def extract_vid(video):
    try:
        vid = ffmpeg.probe(video)
        #print(vid['streams'][0]['tags']['creation_time'])
        date = vid['streams'][0]['tags']['creation_time']
        year = date[0]+date[1]+date[2]+date[3]
        month = date[5]+date[6]
        day = date[8]+date[9]
        return year,month,day
    except:
        return None

def get_field(exif,field):
    try:
        for (k,v) in exif.items():
            if ExifTags.TAGS.get(k) == field:
                return v
    except:
        #print("Exif Not Found")
        return None

def no_names(filename):
    try:
        if filename[0]+filename[1]+filename[2] == "VID":
            year = filename[4]+filename[5]+filename[6]+filename[7]
            month = filename[8]+filename[9]
            day = filename[10]+filename[11]
        elif filename[0:11] == "Screenshot_":
            year = filename[11:15]
            month = filename[16:18]
            day = filename[19:21]
        else:
            raise Exception
        return year, month, day
    except:
        return None

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


im_extensions = (".jpeg", ".jpg", ".png", ".gif")
vid_extensions = (".mp4", ".mov", ".avi")

path = config('saved_path')
storage_path = config('misc_path')
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


## Check hash to find duplicates (EXPERIMENTAL)
#hash_img = []
#hash_img_names
#hash_vid = []
#hash_vid_names = []
#hashcheck(vid_files, vid_files_names, im_files, im_files_names) # WHAT VARIABLE?

for image, name in zip(im_files, im_files_names):
    #print(image)
    exif = extract(image)
    if exif == None:
        try:
            year, month, day = no_names(name)
            new_path = storage_path+"/"+year+"/"+month+"/"+day+"/"+name
        except:
            new_path = storage_path+"/nodate/"+name
            noname += 1
        print(image, new_path)
        os.rename(image, new_path)
        continue
    field = get_field(exif,"DateTimeOriginal")
    if field == None:
        try:
            year, month, day = no_names(name)
            new_path = storage_path+"/"+year+"/"+month+"/"+day+"/"+name
        except:
            new_path = storage_path+"/nodate/"+name
            noname += 1
        print(image, new_path)
        os.rename(image, new_path)
        continue
    else:
        year = field[0]+field[1]+field[2]+field[3]
        month = field[5]+field[6]
        day = field[8]+field[9]
        new_path = storage_path+"/"+year+"/"+month+"/"+day+"/"+name
    print(image, new_path)
    os.rename(image, new_path)

for video, name in zip(vid_files, vid_files_names):
    try:
        year, month, day = extract_vid(video)
        new_path = storage_path+"/"+year+"/"+month+"/"+day+"/"+name
        print(video, new_path)
        os.rename(video, new_path)
    except:
        #print("No Date")
        try:
            year, month, day = no_names(name)
            new_path = storage_path+"/"+year+"/"+month+"/"+day+"/"+name
        except:
            noname += 1
            new_path = storage_path+"/nodate/"+name
        print(video, new_path)
        os.rename(video, new_path)
print(noname)
