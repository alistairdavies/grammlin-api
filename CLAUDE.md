# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Swedish grammar analysis API built with FastAPI. It provides linguistic analysis of Swedish text including part-of-speech tagging, morphological analysis, and dictionary definitions from Folkets Lexikon.

## Development Commands

### Setup
```bash
# Create and activate virtual environment
uv venv
source venv/bin/activate  # or: source venv/bin/activate.fish

# Install dependencies
uv install

# Install required NLP models (must be done after installation)
uv run python -m spacy download sv_core_news_lg
uv run python -m uralicNLP.download --languages swe
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
  - `main.py` - API app initialization and router registration
  - `analyse.py` - `/analyse` endpoint with request/response types
  - `define.py` - `/define` endpoint with request/response types

- **`language/analysis/`** - Core linguistic analysis
  - `parser.py` - Main parsing logic, orchestrates token analysis
  - `part_of_speech.py` - Maps Universal POS tags to application-specific PartOfSpeech types
  - `morphology.py` - Morphological analysis for nouns, verbs, and pronouns (gender, tense, case, etc.)
  - `types.py` - Literal types for all domain types (POS IDs, morphological features)
  - `tokens.py` - Token models (BaseToken, NounToken, VerbToken, PronounToken)
  - `models.py` - Loads the spaCy Swedish model (sv_core_news_lg)

- **`language/dictionary/`** - Dictionary integration
  - `service.py` - DictionaryService loads and searches the XDXF dictionary file

- **`language/detection.py`** - Language detection
  - `is_swedish()` - Validates that text is Swedish using lingua-py

- **`tests/`** - Unit tests mirror the language module structure

### Data Flow

1. **Request** → FastAPI receives text via `/parse` endpoint (api/main.py:26)
2. **Validation** → Input is validated:
   - Pydantic validates length (1-1000 chars) and strips whitespace
   - Language detection confirms text is Swedish (returns 422 if not)
3. **NLP Processing** → spaCy processes text with Swedish model
4. **Token Parsing** → Each token is analyzed:
   - Part-of-speech mapping from Universal POS tags
   - Morphological analysis based on POS type (noun/verb/pronoun)
   - Dictionary lookup using lemmatized form with POS filtering
   - Punctuation tokens are filtered out
5. **Response** → Returns typed tokens with morphology and definitions

### Token Type System

The parser returns different token types based on part-of-speech:
- **NounToken** - includes NounMorphology (gender, definiteness, plurality)
- **VerbToken** - includes VerbMorphology (tense, form)
- **PronounToken** - includes PronounMorphology (case/form)
- **BaseToken** - fallback for other parts of speech

All token types inherit from BaseToken which provides: text, part_of_speech, and definitions fields.

### Dictionary Integration

The application requires `folkets_sv_en.xdxf` dictionary file in the root directory. This is loaded at startup by DictionaryService and searched using lemmatized word forms. The dictionary is parsed from XDXF format and stored in memory as a dict mapping headwords to lists of DictionaryEntry objects.

**POS-Aware Filtering**: Dictionary searches support optional POS filtering (language/dictionary/service.py). When a POS filter is provided:
1. Returns only definitions matching the detected part of speech (e.g., verb definitions for verbs)
2. Falls back to all definitions if no POS match is found
3. Dictionary POS abbreviations (nn, vb, jj, etc.) are mapped to application POS IDs via `DICTIONARY_POS_MAP`

This ensures users see contextually relevant definitions while maintaining robustness when POS tags are missing or ambiguous.

### Morphological Analysis

Morphology extraction uses `.build()` class methods (language/analysis/morphology.py) that map spaCy's morphological features to application-specific literal types. Unknown or missing values default to None rather than failing.

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
- **Universal POS → Application**: `UNIVERSAL_POS_MAP` in `part_of_speech.py` maps spaCy tags
- **Dictionary POS → Application**: `DICTIONARY_POS_MAP` in `dictionary/service.py` maps Folkets Lexikon abbreviations
- Both mappings reference the canonical `PartOfSpeechId` type from `types.py`

### API Structure
- **Co-locate types with handlers**: Each endpoint file contains its request/response types and handler function
- **Use APIRouter**: Each endpoint file exports a `router` that gets registered in `main.py`
- **Shared dependencies in main.py**: Global instances (nlp, dictionary_service) are initialized in main.py

### Module Placement Guidelines
- **Domain logic belongs in `language/` modules, not `api/`**: Language detection, validation logic, and linguistic operations should live in the language package
- **API layer is thin**: API endpoints should orchestrate calls to language modules and handle HTTP concerns (status codes, request/response models)
- **Keep interfaces minimal**: Only expose what's needed. Prefer single-purpose functions (e.g., `is_swedish()`) over multi-function modules
- **Handle errors at domain boundaries**: Domain modules should return simple values (bool, None) rather than raise exceptions when possible. Let the API layer decide HTTP responses
- **No circular dependencies**: Domain layer (language/) should never import from API layer (api/)

### Adding New Features
When adding features that involve multiple definition sources or POS-dependent behavior:
1. Consider whether filtering/fallback logic is needed
2. Test edge cases: missing data, ambiguous tags, multiple matches
3. Maintain backward compatibility where possible (e.g., optional parameters with sensible defaults)
4. Place domain logic in appropriate `language/` modules, not in the API layer

### Input Validation Pattern
When adding API validation:
1. **Pydantic validators** handle basic constraints (length, format, whitespace trimming)
2. **Domain-specific validation** goes in `language/` modules (e.g., language detection)
3. **API returns 422** for validation failures with descriptive error messages
4. **Domain functions return simple types** (bool, None, str) - avoid raising exceptions for expected failure cases

Example: The `is_swedish()` function returns `False` instead of raising an exception, allowing the API layer to decide the appropriate HTTP response.

## Dependencies

- **FastAPI/Uvicorn** - Web framework and ASGI server
- **spaCy** - NLP pipeline with `sv_core_news_lg` model for Swedish
- **uralicNLP** - Additional Swedish language resources
- **lingua-py** - Language detection for Swedish validation (optimized for short texts)
- **Pydantic** - Data validation and serialization
- **pytest** - Testing framework
- **ruff** - Linting and formatting

## Git Conventions

- Keep commits meaningful and focused on logical chunks
- Ask which files to include/exclude when creating commits
- Use short, concise one-line commit messages
- Omit Claude Code attribution from commit messages
- Proactively remove dead or commented out code
