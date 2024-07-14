import random
from dataclasses import dataclass
from enum import StrEnum

from src.utils import load_conf, read_txt_file


class PlayerType(StrEnum):
    USER = "user"
    PIRATE = "pirate"


@dataclass
class Player:
    kind: PlayerType
    name: str
    score: int = 0


class User(Player):
    def __init__(self, name: str):
        if name is None:
            name = input("Write your name.\n")
        super().__init__(kind=PlayerType.USER, name=name)


class Pirate(Player):
    def __init__(self):
        super().__init__(kind=PlayerType.PIRATE, name=self._get_random_pirate_name())

    @staticmethod
    def _get_random_pirate_name() -> str:
        paths = load_conf()
        pirate_types = read_txt_file(
            paths["PATH_TO_PIRATE_TYPES_ORIGINAL"], as_list=True
        )
        pirate_types = pirate_types + read_txt_file(
            paths["PATH_TO_PIRATE_TYPES_GENERATED"], as_list=True
        )
        pirate_types = list(set(pirate_types))
        random.shuffle(pirate_types)
        return random.choice(pirate_types)


def get_pirate_types(
    subsets: list[str] = ["original"], as_string: bool = False, seed: int = 31
):
    paths = load_conf()
    pirate_types = []
    if "original" in subsets:
        pirate_types = pirate_types + read_txt_file(
            paths["PATH_TO_PIRATE_TYPES_ORIGINAL"], as_list=True
        )
    if "generated" in subsets:
        pirate_types = pirate_types + read_txt_file(
            paths["PATH_TO_PIRATE_TYPES_GENERATED"], as_list=True
        )
    pirate_types = list(set(pirate_types))
    random.seed(seed)
    random.shuffle(pirate_types)
    if as_string:
        return ", ".join(pirate_types)
    else:
        return pirate_types
