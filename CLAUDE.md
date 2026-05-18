# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Swedish grammar analysis API built with FastAPI. It provides linguistic analysis of Swedish text including part-of-speech tagging, morphological analysis, and dictionary definitions from Folkets Lexikon.

## Development Commands

### Setup
```bash
# Install dependencies
uv sync

# The app uses Stanza by default. The Stanza Swedish model is downloaded
# automatically at startup on first run.

# To use SpacyNLPAnalyser instead, install the Swedish model manually:
uv run python -m spacy download sv_core_news_md
```

### Running the Application
```bash
./scripts/run-app.sh
# API runs on http://localhost:8001 (note: port 8001, not 8000)
```

### Testing
```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/language/analysis/test_morphology.py

# Run specific test class or function
uv run pytest tests/language/analysis/test_morphology.py::TestNounMorphology_build
uv run pytest tests/language/analysis/test_morphology.py::TestNounMorphology_build::test_returns_mapped_valid_values
```

**Test Structure Convention**: Tests must mirror the source directory structure. For example:
- `language/analysis/morphology.py` → `tests/language/analysis/test_morphology.py`
- `language/dictionary/service.py` → `tests/language/dictionary/test_service.py`

### Smoke Tests
Post-deploy quality evaluation against the live API:
```bash
# Against deployed service (default)
python3 scripts/smoke_test.py

# Against local server
python3 scripts/smoke_test.py --url http://localhost:8001

# With custom thresholds
python3 scripts/smoke_test.py --lemma-threshold 0.80 --pos-threshold 0.90
```

Reports lemma accuracy, POS accuracy, and definition coverage across 20 targeted sentences. Exits with code 1 if any metric falls below its threshold.

### Linting and Formatting
```bash
# Lint with auto-fix
uv run ruff check --fix

# Format code
uv run ruff format
```

**Note**: Ruff is configured with line-length=79 and E501 rule enforcement in pyproject.toml.

## Architecture

### Module Organization

The codebase follows a domain-driven structure with clear separation of concerns:

- **`api/`** - FastAPI application layer
  - `main.py` - API app initialization, router registration, and NLP analyser selection
  - `health.py` - `/health` endpoint for health checks
  - `analyse.py` - `/analyse` endpoint with request/response types

- **`language/analysis/`** - Core linguistic analysis
  - `analyser.py` - `NLPAnalyser` protocol defining the analyser interface
  - `part_of_speech.py` - Maps Universal POS tags to application-specific PartOfSpeech types
  - `morphology.py` - Morphological analysis for nouns, verbs, adjectives, and pronouns
  - `types.py` - Literal types for all domain types (POS IDs, morphological features)
  - `tokens.py` - Token models (BaseToken, NounToken, VerbToken, PronounToken, AdjectiveToken)
  - `stanza/` - Stanza-based NLP implementation (default, better accuracy)
  - `spacy/` - spaCy-based NLP implementation (alternative, requires manual model install)

- **`language/dictionary/`** - Dictionary integration
  - `sqlite_store.py` - Searches the SQLite dictionary database by headword and POS
  - `build.py` - Builds the SQLite database from the XDXF source file
  - `models.py` - DictionaryEntry model

- **`language/detection.py`** - Language detection
  - `is_swedish()` - Validates that text is Swedish using lingua-py

- **`tests/`** - Unit tests mirror the language module structure

### NLP Backend

The application supports two NLP backends via the `NLPAnalyser` protocol:

- **Stanza** (`StanzaNLPAnalyser`) — currently deployed. Better lemmatization and POS accuracy, higher memory usage (~870MB in Docker).
- **spaCy** (`SpacyNLPAnalyser`) — alternative backend. Lower memory usage but weaker lemmatization, particularly on irregular verb forms. Requires `sv_core_news_md` to be installed manually (not a project dependency).

Switch backends by changing the analyser instantiated in `api/main.py`.

### Data Flow

1. **Request** → FastAPI receives text via `/analyse` endpoint
2. **Validation** → Input is validated:
   - Pydantic validates length (1-1000 chars) and strips whitespace
   - Language detection confirms text is Swedish (returns 422 if not)
3. **NLP Processing** → Stanza (or spaCy) processes text with Swedish model
4. **Token Parsing** → Each token is analyzed:
   - Part-of-speech mapping from Universal POS tags
   - Morphological analysis based on POS type (noun/verb/adjective/pronoun)
   - Dictionary lookup using lemmatized form with POS filtering
   - Punctuation tokens are filtered out
5. **Response** → Returns typed tokens with morphology and definitions

### Token Type System

The parser returns different token types based on part-of-speech:
- **NounToken** - includes NounMorphology (gender, definiteness, plurality)
- **VerbToken** - includes VerbMorphology (tense, form)
- **AdjectiveToken** - includes AdjectiveMorphology (degree)
- **PronounToken** - includes PronounMorphology (case/form)
- **BaseToken** - fallback for other parts of speech

All token types inherit from BaseToken which provides: text, lemma, part_of_speech, and definitions fields.

### Dictionary Integration

The application uses a SQLite database (`folkets_sv_en.db`) built from the Folkets Lexikon XDXF file. The database is built at image build time by `scripts/build.sh` and is not committed to the repository.

**POS-Aware Filtering**: Dictionary searches filter by POS to return contextually relevant definitions. When a POS filter is provided:
1. Returns only definitions matching the detected part of speech
2. Falls back to null-POS entries if no POS match is found
3. Dictionary POS abbreviations (nn, vb, jj, etc.) are mapped to application POS IDs via `DICTIONARY_POS_MAP` in `sqlite_store.py`

### Morphological Analysis

Morphology extraction uses `.build()` class methods (language/analysis/morphology.py) that map morphological feature strings to application-specific literal types. Unknown or missing values default to None rather than failing.

## Code Conventions

### Comments
- **Comments explain "why", not "what"**: Code should be self-explanatory; comments clarify intent or reasoning
- **Use comments sparingly**: Only when the logic isn't self-evident
- **No separator comments**: Avoid `# === Section ===` style comments that just label sections

### Type Definitions
- All Literal types for domain values are centralized in `language/analysis/types.py`
- This includes `PartOfSpeechId` and morphological feature types
- Use string Literal types rather than Enums for simple value constraints
- Token models (BaseToken, NounToken, etc.) live in `language/analysis/tokens.py`
- Separation prevents circular imports between types, morphology, and part_of_speech modules

### Part of Speech Mappings
- **Universal POS → Application**: `UNIVERSAL_POS_MAP` in `part_of_speech.py` maps spaCy/Stanza tags
- **Dictionary POS → Application**: `DICTIONARY_POS_MAP` in `sqlite_store.py` maps Folkets Lexikon abbreviations
- Both mappings reference the canonical `PartOfSpeechId` type from `types.py`

### API Structure
- **Co-locate types with handlers**: Each endpoint file contains its request/response types and handler function
- **Use APIRouter**: Each endpoint file exports a `router` that gets registered in `main.py`
- **Shared dependencies in main.py**: Global instances (analyser, dictionary_store) are initialized in main.py

### Module Placement Guidelines
- **Domain logic belongs in `language/` modules, not `api/`**: Language detection, validation logic, and linguistic operations should live in the language package
- **API layer is thin**: API endpoints should orchestrate calls to language modules and handle HTTP concerns (status codes, request/response models)
- **Keep interfaces minimal**: Only expose what's needed. Prefer single-purpose functions (e.g., `is_swedish()`) over multi-function modules
- **Handle errors at domain boundaries**: Domain modules should return simple values (bool, None) rather than raise exceptions when possible. Let the API layer decide HTTP responses
- **No circular dependencies**: Domain layer (language/) should never import from API layer (api/)

### Input Validation Pattern
When adding API validation:
1. **Pydantic validators** handle basic constraints (length, format, whitespace trimming)
2. **Domain-specific validation** goes in `language/` modules (e.g., language detection)
3. **API returns 422** for validation failures with descriptive error messages
4. **Domain functions return simple types** (bool, None, str) - avoid raising exceptions for expected failure cases

## Dependencies

### Production Dependencies
- **FastAPI/Uvicorn** - Web framework and ASGI server
- **Stanza** - Primary NLP pipeline (Stanford NLP), Swedish model downloaded at startup
- **spaCy** - Alternative NLP pipeline; `sv_core_news_md` model not installed by default
- **lingua-py** - Language detection for Swedish validation (optimized for short texts)
- **Pydantic** - Data validation and serialization

### Development Dependencies
- **pytest** - Testing framework
- **ruff** - Linting and formatting

## Deployment

The application is deployed to Fly.io using Docker.

### Deployment Files

- **`fly.toml`** - Fly.io service configuration
  - Region: `arn` (Stockholm)
  - Machine: 1GB RAM (shared CPU)
  - Auto-stop when idle, auto-start on request

- **`Dockerfile`** - Multi-stage build
  - Builder stage: installs dependencies, downloads XDXF, builds SQLite database, downloads Stanza model
  - App stage: copies only runtime artifacts (venv, app code, database, Stanza models)

- **`scripts/build.sh`** - Build script run during Docker image build
  - Installs dependencies via `uv sync --no-dev`
  - Downloads Folkets Lexikon XDXF and builds SQLite database
  - Downloads Stanza Swedish model

- **`THIRD_PARTY_NOTICES.md`** - License attributions for Folkets Lexikon, Stanza, and spaCy models

### CI/CD

- **`.github/workflows/ci.yml`** - Runs lint, type-check, and tests on push and PRs to main
- **`.github/workflows/deploy.yml`** - Deploys to Fly.io when CI passes on main
- **`.github/workflows/smoke-test.yml`** - Manual workflow to run post-deploy quality checks

### Deployment Process

Push to main triggers CI. On success, the deploy workflow builds and pushes the Docker image to Fly.io automatically. The `FLY_API_TOKEN` secret must be set in the GitHub repository settings.

### Running Smoke Tests After Deploy

```bash
python3 scripts/smoke_test.py
```

The service auto-stops when idle. First request after inactivity will be slower as Fly.io starts the machine.

## Git Conventions

- Keep commits meaningful and focused on logical chunks
- Ask which files to include/exclude when creating commits
- Use short, concise one-line commit messages
- Omit Claude Code attribution from commit messages
- Proactively remove dead or commented out code
