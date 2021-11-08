# hash_checker (brute version)
# Version 3.0

import lib.hash as hash_ut #this is to prevent variable with same name...
import os
import lib.create_tree as create_tree
# import environment variables
from decouple import config

path = config('import_path')
discarded_path  = config('discarded_path')
saved_path = config('saved_path')
files = []
filesnames = []
hash_files = []
number = 0
discarded = []
discarded_name = []
saved = []
saved_name = []
save_hash = []

files, filesnames = create_tree.create_tree(path)
'''imported above as create_tree.create_tree
for root, d_names, f_names in os.walk(path):
    for f in f_names:
        # if f.endswith(im_extensions):
        #     im_files.append(os.path.join(root,f))
        #     im_files_names.append(f)
        # elif f.endswith(vid_extensions):
        #     vid_files.append(os.path.join(root,f))
        #     vid_files_names.append(f)
        files.append(os.path.join(root,f))
        filesnames.append(os.path.join(f))
'''
with open(config('hash_files_dict'),'r') as hashes:
    #hash_files = hashes.readlines()
    hash_files = hashes.read().splitlines()


## check new images - this is slow but since there are not a lot of new images, it is still acceptable
for image,name in zip(files, filesnames):
    it_exists = 0
    print(image)
    hash_image = hash_ut.get_hash(image)
    for hash in hash_files:
        if hash == hash_image:
            discarded.append(image)
            discarded_name.append(name)
            it_exists = 1
        else:
            pass
    if it_exists == 0:
	save_hash(hash_image)
        saved.append(image)
        saved_name.append(name)

print(saved)
print(discarded)

# Discard duplicates photos.
for discard, name in zip(discarded, discarded_name):
    print(discard, name)
    os.rename(discard, os.path.join(discarded_path,name))
# Save new photos.
for save, name in zip(saved, saved_name):
    print(save, name)
    os.rename(save, os.path.join(saved_path,name))
path_hash_files = config('hash_files_dict')
path_hash_names = config('hash_files_names_dict')
with open(path_hash_files, "a") as hashes:
    with open(path_hash_names,"a") as hashes_names:
        for saving, name in zip(save_hash, saved_name):
            nameline = os.path.join(saved_path, name)
            hashes.writelines(saving+"\n")
            hashes_names.writelines(nameline+"\n")
