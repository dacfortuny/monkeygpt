from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from src.mistral_text_generator import MistralTextGenerator


def test_generate_text_extracts_message_content():
    fake_response = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content="Arrr!"))]
    )
    fake_client = MagicMock()
    fake_client.chat.complete.return_value = fake_response

    with (
        patch("src.mistral_text_generator.Mistral", return_value=fake_client),
        patch("src.mistral_text_generator.get_mistral_api_key", return_value="dummy"),
    ):
        generator = MistralTextGenerator(model="open-mistral-7b")
        result = generator.generate_text("Ahoy")

    assert result == "Arrr!"
    fake_client.chat.complete.assert_called_once_with(
        model="open-mistral-7b",
        messages=[{"role": "user", "content": "Ahoy"}],
    )
