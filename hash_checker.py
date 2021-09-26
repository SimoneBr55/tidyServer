# hash_checker (brute version)
# Version 2.0

import hashlib, os
# import environment variables
from decouple import config

def get_hash(full_path):
    return hash_bytestr_iter(file_as_blockiter(open(full_path, 'rb')), hashlib.md5(), True)

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

with open(config('hash_files_dict'),'r') as hashes:
    #hash_files = hashes.readlines()
    hash_files = hashes.read().splitlines()


## check new images
for image,name in zip(files, filesnames):
    it_exists = 0
    print(image)
    hash_image = get_hash(image)
    for hash in hash_files:
        if hash == hash_image:
            discarded.append(image)
            discarded_name.append(name)
            it_exists = 1
        else:
            continue
    if it_exists == 0:
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

with open(config('hash_files_dict'), "a") as hashes:
    with open(config('hash_file_names_dict'),"a") as hashes_names:
        for save, name in zip(saved, saved_name):
            nameline = os.path.join(saved_path, name)
            hashes.writelines(save+"\n")
            hashes_names.writelines(nameline+"\n")
