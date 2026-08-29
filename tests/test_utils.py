import pandas as pd

from src.utils import get_api_key, get_insults, get_list_of_insults


def test_get_api_key_prefers_env_var(tmp_path, monkeypatch):
    key_file = tmp_path / "api_key.yaml"
    key_file.write_text("MY_KEY: from_file\n")
    monkeypatch.setenv("MY_KEY", "from_env")

    assert get_api_key("MY_KEY", str(key_file)) == "from_env"


def test_get_api_key_falls_back_to_file(tmp_path, monkeypatch):
    key_file = tmp_path / "api_key.yaml"
    key_file.write_text("MY_KEY: from_file\n")
    monkeypatch.delenv("MY_KEY", raising=False)

    assert get_api_key("MY_KEY", str(key_file)) == "from_file"


def test_get_insults_returns_dataframe_with_expected_columns():
    insults = get_insults()
    assert isinstance(insults, pd.DataFrame)
    assert list(insults.columns) == ["insult", "answer"]
    assert len(insults) > 0


def test_get_insults_is_cached():
    assert get_insults() is get_insults()


def test_get_list_of_insults_returns_n_tuples():
    insults = get_list_of_insults(3)
    assert len(insults) == 3
    assert all(isinstance(row, tuple) and len(row) == 2 for row in insults)
