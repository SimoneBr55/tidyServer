# hash_start
## This script creates the text file with hash and the file with the corresponding filename.
## This script should be run at start and/or periodically.
## Version 3.0

import hashlib
import os
import shutil

# Import environment variables
from decouple import config

'''-----------------FUNCTION DEFINITION-----------------'''

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

def create_tree(path):
    files = []
    files_names = []
    for root, d_names, f_names in os.walk(path):
        for f in f_names:
                files.append(os.path.join(root,f))
                files_names.append(os.path.join(root,f))
    return files, files_names

def hashing(files):
    hash_files = []
    for file in files:
        hash = get_hash(file)
        hash_files.append(hash)
    return hash_files

def getDuplicatesWithInfo(listOfElems):
    ''' Get duplicate element in a list along with their indices in list
     and frequency count'''
    dictOfElems = dict()
    index = 0
    # Iterate over each element in list and keep track of index
    for elem in listOfElems:
        # If element exists in dict then keep its index in lisr & increment its frequency
        if elem in dictOfElems:
            dictOfElems[elem][0] += 1
            dictOfElems[elem][1].append(index)
        else:
            # Add a new entry in dictionary
            dictOfElems[elem] = [1, [index]]
        index += 1

    dictOfElems = { key:value for key, value in dictOfElems.items() if value[0] > 1}
    return dictOfElems

def correct_duplicates(dictOfElems, files_names, bin):
    try:
        for key, value in dictOfElems.items():
            res_list = [files_names[i] for i in value[1]]
            print('Element = ', key , ' :: Repeated Count = ', value[0] , ' :: Index Positions =  ', value[1], ' :: FilePaths = ', res_list)
            smallest = min(len(entry) for entry in res_list)
            iter = 1
            redo = False
            for rep in res_list:
                if redo == False:
                    if len(rep) == smallest:
                        ext = os.path.splitext(rep)[1]
                        shutil.copy(rep,os.path.join(bin,key[0:5]+"0"+ext))
                        redo = True
                    else:
                        ext = os.path.splitext(rep)[1]
                        os.rename(rep,os.path.join(bin,key[0:5]+str(iter)+ext))
                        iter += 1
                else:
                    ext = os.path.splitext(rep)[1]
                    os.rename(rep,os.path.join(bin,key[0:5]+str(iter)+ext))
                    iter += 1
        return 0
    except:
        return 1

def write_files(hash_files, files_names):
    try:
        with open(config('hash_files_dict'), "w") as out:
            for hash in hash_files:
                out.writelines(hash+"\n")
        with open(config('hash_files_names_dict'), "w") as outnames:
            for name in files_names:
                outnames.writelines(name+"\n")
        return 0
    except:
        return 1
'''-----------------ACTUAL WORKFLOW CODE-----------------'''
# Actual algorithmic code
path = config('start_path')
bin = config('discarded_path')
iter = 0
stopping  = False
while stopping == False:
    iter += 1
    print("Run ", iter)
    files, files_names = create_tree(path)
    hash_files = hashing(files)
    dictOfElems = getDuplicatesWithInfo(hash_files)
    if dictOfElems == {}:
        stopping = True
    if (correct_duplicates(dictOfElems, files_names, bin)):
        print("Error Correcting Duplicates")
        exit()
    else:
        pass
write_files(hash_files, files_names)
