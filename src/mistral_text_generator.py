from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

from src.utils import get_mistral_api_key


class MistralTextGenerator:
    API_KEY = get_mistral_api_key()

    def __init__(self, model="open-mistral-7b"):
        self.model = model
        self.client = MistralClient(api_key=MistralTextGenerator.API_KEY)

    def _call_mistral(self, prompt):
        return self.client.chat(
            model=self.model, messages=[ChatMessage(role="user", content=prompt)]
        )

    def generate_text(self, prompt):
        response = self._call_mistral(prompt)
        return response.choices[0].message.content
