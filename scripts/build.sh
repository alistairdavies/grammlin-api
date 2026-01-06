#!/usr/bin/env bash
set -e

echo "Installing dependencies..."
pip install uv
uv install

echo "Downloading spaCy Swedish model..."
uv run python -m spacy download sv_core_news_lg

echo "Downloading dictionary file..."
curl -L -o folkets_sv_en.xdxf https://folkets-lexikon.csc.kth.se/folkets/folkets_sv_en_public.xdxf

echo "Build complete!"
