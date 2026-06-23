# Grammlin API

A Swedish grammar analysis API providing part-of-speech tagging, morphological analysis, and dictionary definitions from [Folkets Lexikon](https://folkets-lexikon.csc.kth.se/folkets/om.html). Uses [Stanza](https://stanfordnlp.github.io/stanza/) (default) or [spaCy](https://spacy.io/models/sv) for NLP.

- [Chrome Extension](https://chromewebstore.google.com/detail/grammlin/emipiahcdgnnlopmohkaedhbobgcaleo)
- [Firefox Addon](https://addons.mozilla.org/en-US/firefox/addon/grammlin/)

## Local Development

1. Install dependencies:
```sh
uv sync
```

2. Activate the virtual environment:
Bash:
```sh
source venv/bin/activate
```

Fish:
```sh
source venv/bin/activate.fish
```

3. Install Dependencies
```sh
uv sync
```

4. Build the dictionary database

Download `folkets_sv_en.xdxf` from https://folkets-lexikon.csc.kth.se/folkets/folkets_sv_en_public.xdxf and place it in the project root, then run:
```sh
uv run python -m language.dictionary.build
```

5. Run the app
```sh
./scripts/run-app.sh
```

The API is available at http://localhost:8001. The Stanza Swedish model downloads automatically on first startup.

### Using spaCy instead

Switch the analyser in `api/main.py` from `StanzaNLPAnalyser` to `SpacyNLPAnalyser`.

## Linting and Formatting

```sh
uv run ruff check --fix   # lint with auto-fix
uv run ruff format        # format
```

## Testing

```sh
uv run pytest
```
