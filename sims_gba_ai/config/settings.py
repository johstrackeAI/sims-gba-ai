# Placeholder for settings (API keys, window title, key mappings, etc.)

EMULATOR_WINDOW_TITLE = "mGBA" # Adjust this if your emulator window has a different title
# LLM Interaction Settings
LLM_PROVIDER = "lmstudio"  # Options: "lmstudio", "openrouter"

# lmstudio Configuration (if LLM_PROVIDER is "lmstudio")
LMSTUDIO_API_BASE = "http://localhost:1234/v1"
# No API key needed for local lmstudio typically
# Model is usually selected in the lmstudio UI, not via API param

# OpenRouter Configuration (if LLM_PROVIDER is "openrouter")
OPENROUTER_API_KEY = "YOUR_API_KEY"  # Replace with your actual OpenRouter API key
OPENROUTER_API_BASE = "https://openrouter.ai/api/v1"
LLM_MODEL = "openai/gpt-4-vision-preview" # Example model, adjust as needed for OpenRouter

# Valid GBA Buttons for LLM Suggestion
VALID_GBA_BUTTONS = ["Up", "Down", "Left", "Right", "A", "B"]
# Input Simulation Settings
GBA_KEY_MAPPINGS = {
    "Up": "up",
    "Down": "down",
    "Left": "left",
    "Right": "right",
    "A": "x",
    "B": "z",
    "L": "a",
    "R": "s",
    "Start": "enter",
    "Select": "backspace"
}
KEY_PRESS_PAUSE = 0.1 # Seconds to pause after a key press
# Delay between main loop iterations in seconds
LOOP_DELAY = 2