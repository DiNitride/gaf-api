from os import getenv, getcwd
import pathlib
import json

def combine(**kwargs):
    return kwargs

def load_config(filename: str):
    base = getenv("CONFIG_BASE", getcwd() + "/config")

    with open(pathlib.Path(base, filename)) as fp:
        return json.load(fp)
