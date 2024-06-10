import random

from src.utils import load_conf, read_txt_file


class Player:
    def __init__(self, name=None, type=None):
        self.name = name
        self.type = type
        self.score = 0


class User(Player):
    def __init__(self, name):
        if name is None:
            self.name = input('Write your name.\n')
        else:
            self.name = name
        super().__init__(self.name, type="user")


class Pirate(Player):
    def __init__(self):
        self.name = self._get_random_pirate_name()
        super().__init__(name=self.name, type="pirate")

    def _get_random_pirate_name(self):
        paths = load_conf()
        pirate_types = read_txt_file(paths["PATH_TO_PIRATE_TYPES_ORIGINAL"], as_list=True)
        pirate_types = pirate_types + read_txt_file(paths["PATH_TO_PIRATE_TYPES_GENERATED"], as_list=True)
        pirate_types = list(set(pirate_types))
        random.shuffle(pirate_types)
        return random.choice(pirate_types)


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
