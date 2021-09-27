import hashlib
from lxml import etree


def sha256sum(filename):
    h  = hashlib.sha256()
    b  = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        for n in iter(lambda : f.readinto(mv), 0):
            h.update(mv[:n])
        return h.hexdigest()


def get_xml_tree(filepath):
    memory_file_and_hash = {}

    def memorize_file_and_hash():
        file_hash = sha256sum(filepath)

        if file_hash == memory_file_and_hash.get(file_hash):
            return memory_file_and_hash.get('tree')
        else:
            tree = etree.parse(filepath)
            memory_file_and_hash['file_hash'] = file_hash
            memory_file_and_hash['tree'] = tree
            return tree

    return memorize_file_and_hash
