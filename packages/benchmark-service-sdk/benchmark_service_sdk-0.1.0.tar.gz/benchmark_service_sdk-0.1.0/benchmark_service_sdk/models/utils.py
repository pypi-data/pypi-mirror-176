import os
import pathlib
from typing import Union
from urllib.request import urlopen


def read_local_file_or_url(file_path_or_url: Union[pathlib.Path, str]):
    assert file_path_or_url

    if os.path.isfile(file_path_or_url):
        with open(file_path_or_url, 'r') as run_in:
            return run_in.read()
    else:
        return urlopen(file_path_or_url).read().decode('utf-8')
