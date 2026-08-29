import random

from src.players import get_pirate_types


def test_get_pirate_types_original_subset():
    original = get_pirate_types(subsets=["original"])
    with open("resources/data/pirate_types_original.txt") as f:
        expected = set(f.read().splitlines())
    assert set(original) == expected


def test_get_pirate_types_as_string():
    result = get_pirate_types(subsets=["original"], as_string=True)
    assert isinstance(result, str)
    assert ", " in result


def test_get_pirate_types_seed_is_deterministic():
    first = get_pirate_types(subsets=["original", "generated"], seed=7)
    second = get_pirate_types(subsets=["original", "generated"], seed=7)
    assert first == second


def test_get_pirate_types_does_not_pollute_global_random_state():
    random.seed(123)
    expected_next = random.random()

    random.seed(123)
    get_pirate_types(subsets=["original"], seed=999)
    actual_next = random.random()

    assert actual_next == expected_next
