from mistralai import Mistral

from src.utils import get_mistral_api_key


class MistralTextGenerator:
    def __init__(self, model="mistral-small-latest"):
        self.model = model
        self.client = Mistral(api_key=get_mistral_api_key())

    def _call_mistral(self, prompt, temperature, presence_penalty):
        return self.client.chat.complete(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            presence_penalty=presence_penalty,
        )

    def generate_text(self, prompt, temperature=1.0, presence_penalty=0.5):
        response = self._call_mistral(prompt, temperature, presence_penalty)
        return response.choices[0].message.content
