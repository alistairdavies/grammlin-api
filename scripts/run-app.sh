#!/bin/bash

uvicorn api.main:api --host 0.0.0.0 --port 8001 --reload
