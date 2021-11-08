##---------------------hash_start------------------##
## This script creates the text file with hash and the file with the corresponding filename.
## This script should be run at start and/or periodically.
## Version 4.0
##-------------------------------------------------##

# Import environment variables
from decouple import config

'''-----------------FUNCTION IMPORT-----------------'''

import lib.duplicates as duplicates
import lib.write_files as write_files
import lib.create_tree as create_tree
import lib.hash as hash

'''----------------ACTUAL WORKFLOW CODE-----------------'''
# Actual algorithmic code
path = config('start_path')
bin = config('discarded_path')
iter = 0
stopping  = False
while stopping == False:
    iter += 1
    print("Run ", iter)
    files, files_names = create_tree.create_tree(path)
    hash_files = hash.hashing(files)
    dictOfElems = duplicates.getInfo(hash_files)
    print(dictOfElems)
    if dictOfElems == {}:
        stopping = True
    if (duplicates.correct_duplicates(dictOfElems, files_names, bin)):
        print("Error Correcting Duplicates")
        exit()
    else:
        pass
hash_files_dict = config('hash_files_dict')
hash_files_names_dict = config('hash_files_names_dict')
write_files.write_files(hash_files, files_names, hash_files_dict, hash_files_names_dict)
print(dictOfElems)
