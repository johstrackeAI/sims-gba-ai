# Sims 2 GBA AI Controller

## Overview

This project aims to control The Sims 2 on Game Boy Advance (GBA) using an AI. Phase 1 focuses on capturing the emulator screen, sending the image (or OCR text) to a Large Language Model (LLM) to decide the next button press, and simulating that press.

## Setup

1.  **Create and activate a Python virtual environment:**
    *   On Windows:
        ```bash
        python -m venv .venv
        .\.venv\Scripts\activate
        ```
    *   On macOS/Linux:
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Key settings are located in `sims_gba_ai/config/settings.py`. You **must** configure the following before running:

*   `EMULATOR_WINDOW_TITLE`: The exact title of the emulator window running the game.
*   LLM Provider Details:
    *   `LLM_PROVIDER`: Set to your chosen provider (e.g., 'openai', 'anthropic', 'ollama').
    *   API Keys/URLs: Configure the relevant API key (e.g., `OPENAI_API_KEY`) or base URL (e.g., `OLLAMA_BASE_URL`).
    *   `LLM_MODEL`: Specify the model to use (e.g., 'gpt-4o', 'claude-3-opus-20240229', 'llama3').
*   `GBA_KEY_MAPPINGS`: Ensure the key codes match your emulator's configuration if you've changed them from the defaults (relevant for `win32` input simulation).

## Running

1.  Start your GBA emulator (e.g., mGBA) and load The Sims 2 GBA ROM.
2.  Make sure your virtual environment is activated (`.venv`).
3.  Run the main script from the project root directory:
    ```bash
    python -m sims_gba_ai.main
