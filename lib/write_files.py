def write_files(hash_files, files_names, hash_files_dict, hash_files_names_dict):
    try:
        with open(hash_files_dict, "w") as out:
            for hash in hash_files:
                out.writelines(hash+"\n")
        with open(hash_files_names_dict, "w") as outnames:
            for name in files_names:
                outnames.writelines(name+"\n")
        return 0
    except:
        return 1

def quick_write(path,line):
    try:
	with open(path,"w") as file:
            file.writelines(line+"\n")
        return 0
    except:
        return 1
