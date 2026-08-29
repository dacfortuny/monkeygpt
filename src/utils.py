import csv
import os
from functools import lru_cache

import pandas as pd
from omegaconf import OmegaConf

PATH_TO_CONF = "src/config.yaml"
PATH_TO_API_KEY = "api_key.yaml"


def load_conf(path_to_conf=PATH_TO_CONF):
    return OmegaConf.load(path_to_conf)


def get_api_key(key_name, path_to_api_key=PATH_TO_API_KEY):
    return os.environ.get(key_name) or OmegaConf.load(path_to_api_key)[key_name]


def get_mistral_api_key(path_to_api_key=PATH_TO_API_KEY):
    return get_api_key("MISTRAL_API_KEY", path_to_api_key)


def get_telegram_api_key(path_to_api_key=PATH_TO_API_KEY):
    return get_api_key("TELEGRAM_API_KEY", path_to_api_key)


def read_txt_file(path_to_file, as_list=False):
    with open(path_to_file) as file:
        if not as_list:
            return file.read()
        return file.read().splitlines()


def csv_to_list_of_tuples(path_to_file):
    data = []
    with open(path_to_file, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter="|")
        for row in reader:
            data.append(tuple(row))
    return data


def get_game_overview():
    path_to_game_overvier = load_conf()["PATH_TO_PROMPT_GAME_OVERVIEW"]
    return read_txt_file(path_to_game_overvier)


@lru_cache(maxsize=1)
def get_insults():
    paths_to_insults = load_conf()["PATH_TO_INSULTS"]
    insults = pd.concat(
        (pd.read_csv(path, sep="|") for path in paths_to_insults), ignore_index=True
    )
    return insults.drop_duplicates(subset="insult", keep="first").reset_index(drop=True)


def get_insult_cache_path():
    return load_conf()["PATH_TO_INSULT_CACHE"]


def get_list_of_insults(n):
    insults = get_insults()
    return list(insults.sample(n).itertuples(index=False, name=None))
