from mistralai import Mistral

from src.utils import get_mistral_api_key


class MistralTextGenerator:
    def __init__(self, model="open-mistral-7b"):
        self.model = model
        self.client = Mistral(api_key=get_mistral_api_key())

    def _call_mistral(self, prompt):
        return self.client.chat.complete(
            model=self.model, messages=[{"role": "user", "content": prompt}]
        )

    def generate_text(self, prompt):
        response = self._call_mistral(prompt)
        return response.choices[0].message.content
