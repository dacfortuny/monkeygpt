# MI: Battles of the Northwest Wind

An LLM-powered insult sword fighting game. You trade insults and comebacks
with a randomly-named pirate; a [Mistral](https://mistral.ai/) model
generates the pirate's insults and comebacks and judges whether yours land.
Playable from the command line or as a Telegram bot.

## Requirements

- Python >=3.9
- [uv](https://docs.astral.sh/uv/)
- A [Mistral API key](https://console.mistral.ai/)

## Set up

1. Install dependencies:

   ```
   uv sync
   ```

2. Provide your Mistral API key, either by copying the template...

   ```
   cp api_key_template.yaml api_key.yaml
   ```

   ...and filling in `MISTRAL_API_KEY`, or by setting it as an environment
   variable instead (takes precedence over the file):

   ```
   export MISTRAL_API_KEY=your-key-here
   ```

## Play

Run the following command and follow the instructions:

```
uv run python play.py
```

## Telegram bot

The game can also be played as a Telegram bot. Set `TELEGRAM_API_KEY` in
`api_key.yaml` (or as an environment variable) alongside your Mistral key,
then run:

```
uv run python run_bot_server.py
```

Once running, talk to the bot with `/insult <your insult>` and `/help`.

## Development

Run the test suite:

```
uv run pytest
```

Lint and format:

```
uv run ruff check .
uv run ruff format .
```

## Third-party licenses

This project depends on the following, all of which permit ordinary use as
a dependency (no license file or attribution needs to be shipped just to
run this project):

| Package              | License      |
| -------------------- | ------------ |
| mistralai             | Apache-2.0   |
| pandas                | BSD-3-Clause |
| omegaconf             | BSD-3-Clause |
| StrEnum               | MIT          |
| python-telegram-bot   | LGPL-3.0-only |

`python-telegram-bot` is LGPL-3.0, the only copyleft license in the list.
It only imposes obligations (shipping its license text, allowing the
library to be relinked/replaced) if this project is ever redistributed as
a bundled/compiled application rather than run from source via uv — not
relevant for using it as-is.
