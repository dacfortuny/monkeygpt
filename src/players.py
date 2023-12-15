import random

from src.utils import load_conf, read_txt_file


class Player:
    def __init__(self, name, type):
        self.name = name
        self.type = type


class User(Player):
    def __init__(self, name):
        super().__init__(name, type="user")


class Pirate(Player):
    def __init__(self, name):
        super().__init__(name, type="pirate")


def get_pirate_types(subsets=["original"], as_string=False, seed=31):
    paths = load_conf()
    pirate_types = []
    if "original" in subsets:
        pirate_types = pirate_types + read_txt_file(paths["PATH_TO_PIRATE_TYPES_ORIGINAL"],
                                                    as_list=True)
    if "generated" in subsets:
        pirate_types = pirate_types + read_txt_file(paths["PATH_TO_PIRATE_TYPES_GENERATED"],
                                                    as_list=True)
    pirate_types = list(set(pirate_types))
    random.seed(seed)
    random.shuffle(pirate_types)
    if as_string:
        return ", ".join(pirate_types)
    else:
        return pirate_types
