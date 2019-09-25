import setuptools, os
from shutil import copy
from counter import default_config_path

setuptools.setup()

exists = [p for p in default_config_path if os.path.isfile(p)]
if len(exists) == 0:
    destination_path = default_config_path[0]
    source_path = "./.counter.toml"

    copy(source_path, destination_path)
