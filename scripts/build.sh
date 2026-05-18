#!/usr/bin/env bash
set -e

echo "Installing dependencies..."
uv sync --no-dev

echo "Downloading Swedish Stanza model..."
uv run python -c "import stanza; stanza.download('sv')"

echo "Downloading dictionary file..."
curl -L -o folkets_sv_en.xdxf https://folkets-lexikon.csc.kth.se/folkets/folkets_sv_en_public.xdxf

echo "Building dictionary database..."
uv run python -m language.dictionary.build

echo "Build complete!"
