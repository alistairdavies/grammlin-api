#!/usr/bin/env bash
set -e

echo "Installing dependencies..."
pip install uv
uv sync --no-dev

echo "Downloading dictionary file..."
curl -L -o folkets_sv_en.xdxf https://folkets-lexikon.csc.kth.se/folkets/folkets_sv_en_public.xdxf

echo "Build complete!"
