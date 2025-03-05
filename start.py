#!/usr/bin/env python
"""
Script to start the FastAPI Blog Application without Docker.
"""
import uvicorn


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
