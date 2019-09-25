import os
import toml
from requests_oauthlib import OAuth1Session
from counter import default_config_path
from typing import Dict

class Config:
    def __init__(self,
                 consumer_key: str,
                 consumer_secret: str,
                 access_token: str,
                 access_secret: str,
                 database_path="",
                 ):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_secret = access_secret

    def __str__(self) -> str:
        return [self.consumer_key, self.consumer_secret,
                self.access_token. self.access_secret]

def get_config_file_path(custom_path_to_config="") -> str:
    path_to_config = custom_path_to_config
    if path_to_config == "":
        exists = [p for p in default_config_path if os.path.isfile(p)]
        if len(exists) == 0:
            print("Config file not found")
            exit(-2)
        else:
            path_to_config = exists[0]

    return path_to_config

def read_config_file(custom_path_to_config="") -> str:
    path_to_config = get_config_file_path(custom_path_to_config)
    try:
        config_file = open(path_to_config, "r")
        config_toml = config_file.read()
        config_file.close()

        return config_toml
    except FileNotFoundError:
        print("Config file not found")
        exit(-2)

def parse_config(config_toml: str) -> Config:
    parsed_config = toml.loads(config_toml)

    return [
        parsed_config["api"]["consumer_key"],
        parsed_config["api"]["consumer_secret"],
        parsed_config["api"]["access_token"],
        parsed_config["api"]["access_secret"]
    ]

def get_config(custom_path_to_config="") -> Config:
    config_toml = read_config_file(custom_path_to_config)
    key = parse_config(config_toml)
    token = OAuth1Session(key[0], key[1], key[2], key[3])
    return token
