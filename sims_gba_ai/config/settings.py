"""
Configuration Settings for the Sims GBA AI Agent.

This file centralizes various settings used throughout the application,
including API keys, file paths, window identifiers, LLM parameters,
and input simulation details. Modify these values to suit your environment
and preferences.
"""

# --- OCR Configuration ---
# Optional: Full path to the Tesseract executable.
# Set this if pytesseract cannot find Tesseract automatically in your system's PATH.
# Example (Windows): r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# Example (Linux/macOS): "/usr/local/bin/tesseract" or "/usr/bin/tesseract"
# Set to None or "" if Tesseract is correctly installed and in the system PATH.
TESSERACT_CMD_PATH: str | None = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# --- Emulator Configuration ---
# The exact title of the emulator window the agent should target.
# Use tools like `pygetwindow.getAllTitles()` to find the correct title if needed.
EMULATOR_WINDOW_TITLE: str = "mGBA"

# --- LLM Interaction Settings ---
# Specify which LLM provider backend to use.
# Options: "lmstudio" (for local models served via LM Studio), "openrouter"
LLM_PROVIDER: str = "lmstudio"

# Configuration for LM Studio (used if LLM_PROVIDER is "lmstudio")
# The base URL of your running LM Studio server's OpenAI-compatible API endpoint.
LMSTUDIO_API_BASE: str = "http://localhost:1234/v1"
# Note: LM Studio typically doesn't require an API key for local access.
# The specific model used is usually selected within the LM Studio application UI.

# Configuration for OpenRouter (used if LLM_PROVIDER is "openrouter")
# !! SECURITY WARNING: Do not commit your actual API key to version control! !!
# Consider using environment variables or a secrets management solution.
OPENROUTER_API_KEY: str = "YOUR_API_KEY_HERE" # Replace with your key
# The base URL for the OpenRouter API.
OPENROUTER_API_BASE: str = "https://openrouter.ai/api/v1"
# The specific model identifier to use on OpenRouter (e.g., "openai/gpt-4-vision-preview").
# Ensure the chosen model supports vision capabilities if needed.
LLM_MODEL: str = "openai/gpt-4-vision-preview"

# --- LLM Output Control ---
# A list of GBA button names that the LLM is allowed to suggest.
# This helps constrain the LLM's output to valid game inputs.
VALID_GBA_BUTTONS: list[str] = ["Up", "Down", "Left", "Right", "A", "B", "L", "R", "Start", "Select"]

# --- Input Simulation Settings ---
# Maps GBA button names (used internally and by the LLM) to the corresponding
# keyboard key names recognized by `pydirectinput`.
# Adjust these mappings based on your emulator's keyboard configuration.
GBA_KEY_MAPPINGS: dict[str, str] = {
    "Up": "up",        # GBA D-Pad Up -> Keyboard Up Arrow
    "Down": "down",    # GBA D-Pad Down -> Keyboard Down Arrow
    "Left": "left",    # GBA D-Pad Left -> Keyboard Left Arrow
    "Right": "right",  # GBA D-Pad Right -> Keyboard Right Arrow
    "A": "x",          # GBA A Button -> Keyboard 'x' key
    "B": "z",          # GBA B Button -> Keyboard 'z' key
    "L": "a",          # GBA L Shoulder -> Keyboard 'a' key
    "R": "s",          # GBA R Shoulder -> Keyboard 's' key
    "Start": "enter",  # GBA Start Button -> Keyboard Enter key
    "Select": "backspace" # GBA Select Button -> Keyboard Backspace key
}

# The duration (in seconds) to pause briefly after simulating a key press.
# Helps prevent inputs from being registered too quickly by the emulator.
KEY_PRESS_PAUSE: float = 0.1

# --- Main Loop Timing ---
# The delay (in seconds) between the end of one main loop iteration and the
# beginning of the next. Controls how frequently the agent acts.
LOOP_DELAY: float = 2.0