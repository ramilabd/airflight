# -*- coding:utf-8 -*-
"""Module parsing xml-file."""


import hashlib
from functools import lru_cache, partial

from lxml import etree

FILE_PATH = './airflight/data/RS_Via-3.xml'


def count_bytes(fileobject, mv):
    """Return the read bytes of the object.

    Args:
        fileobject (_io.FileIO): FileIO (return function "open()")
        mv (bytearray): bytes-like object

    Returns:
        (int): count bytes of fileobject.
    """
    return fileobject.readinto(mv)


def sha256sum(file_path):
    """Return the calculated hash of the file.

    Args:
        file_path (str): path to xml file.

    Returns:
        hash (str): hash of file.
    """
    hash256 = hashlib.sha256()
    mv = memoryview(bytearray(128 * 1024))

    with open(file_path, 'rb', buffering=0) as fileobject:
        partial_count_bytes = partial(count_bytes, fileobject, mv)
        for num in iter(partial_count_bytes, 0):
            hash256.update(mv[:num])
        return hash256.hexdigest()


@lru_cache
def get_xml_tree(file_hash):
    """Return tree of xml file (file object).

    Memoizes file parsing xml data. If the file has not been modified,
    it returns the file object from memory, otherwise it reads the
    file, saves it and returns it.

    Args:
        file_hash (str): hash of the xml-file.

    Returns:
        ElementTree: tree of xml file (file object).
    """
    return etree.parse(FILE_PATH)
