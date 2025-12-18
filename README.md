# Swedish Grammar
## Local Development
1. Create a Python virtual environment:
```sh
uv venv
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
uv install
```

4. Install NLP Model
```sh
uv run python -m spacy download sv_core_news_lg
```

5. Run the app
```sh
./scripts/run-app.sh
```

The API should now be available at http://localhost:8001



## Linting and Formatting

Lint all files and auto-fix issues if possible:
```
uv run ruff check --fix
```

Format all files:
```
uv run ruff format
```
