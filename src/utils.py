import csv

from omegaconf import OmegaConf
from random import sample

PATH_TO_CONF = "src/config.yaml"


def load_conf(path_to_conf=PATH_TO_CONF):
    return OmegaConf.load(path_to_conf)


def read_txt_file(path_to_file, as_list=False):
    with open(path_to_file) as file:
        if not as_list:
            return file.read()
        else:
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


def get_insults():
    path_to_insults = load_conf()["PATH_TO_INSULTS"]
    return csv_to_list_of_tuples(path_to_insults)


def get_list_of_insults(n):
    insults = get_insults()
    return sample(insults, n)


print(get_insults())
