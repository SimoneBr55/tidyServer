import hashlib

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

def hashing(files):
    hash_files = []
    for file in files:
        hash = get_hash(file)
        hash_files.append(hash)
    return hash_files

if __name__ == "__main__":
    print("Work is still in progress...")
    exit()
