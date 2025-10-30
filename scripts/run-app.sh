#!/bin/bash

# Run FastAPI app with uvicorn, enable auto-reload for development
uvicorn api.main:api --host 0.0.0.0 --port 8000 --reload
