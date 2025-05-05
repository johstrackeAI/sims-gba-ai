"""
Input Simulation Module.

Provides functionality to simulate keyboard presses corresponding to GBA buttons,
targeting a specific emulator window. It uses `pydirectinput` for sending
low-level input events and `pygetwindow` to manage window focus. Key mappings
and press timings are configured via `settings.py`.
"""
import pydirectinput
import time
import pygetwindow as gw
import logging
from typing import Optional # Added for type hinting

# Removed find_window and EMULATOR_WINDOW_TITLE imports as they are no longer needed here
# from sims_gba_ai.utils.window_utils import find_window
# from sims_gba_ai.config.settings import EMULATOR_WINDOW_TITLE
from sims_gba_ai.config.settings import GBA_KEY_MAPPINGS, KEY_PRESS_PAUSE # Keep needed imports

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def press_gba_button(emulator_window: Optional[gw.Window], button: str) -> None:
    """Simulates pressing a GBA button mapped to a keyboard key.

    Focuses the target emulator window and sends a key press using
    `pydirectinput`. The mapping from GBA button name (e.g., "A", "UP")
    to the actual keyboard key is defined in `settings.GBA_KEY_MAPPINGS`.

    Args:
        emulator_window: The `pygetwindow` Window object representing the
                         target emulator. If None or invalid, the function logs
                         an error and returns.
        button: The name of the GBA button to press (string). Must be a valid
                key in the `GBA_KEY_MAPPINGS` dictionary.

    Returns:
        None
    """
    if not emulator_window:
        logging.error("Invalid or None emulator window object provided.")
        return

    if button not in GBA_KEY_MAPPINGS:
        logging.error(f"Invalid GBA button: '{button}'. Not found in key mappings.")
        return

    key_to_press = GBA_KEY_MAPPINGS[button]
    window_title = emulator_window.title # Store title for logging clarity

    logging.info(f"Attempting to press GBA button '{button}' (key '{key_to_press}') in window '{window_title}'")

    try:
        # --- Window Focusing ---
        # Ensure the window is not minimized before attempting to activate.
        if emulator_window.isMinimized:
            logging.debug(f"Restoring minimized window: {window_title}")
            emulator_window.restore()
            time.sleep(0.1) # Small delay after restoring

        # Attempt to bring the window to the foreground and give it focus.
        # activate() can sometimes be unreliable depending on OS and window behavior.
        logging.debug(f"Activating window: {window_title}")
        emulator_window.activate()
        time.sleep(0.1) # Short pause to allow the OS to process the focus change.

        # --- Focus Verification (Optional but Recommended) ---
        # Check if the intended window is actually the active one.
        active_window = gw.getActiveWindow()
        if active_window is None or active_window.title != window_title:
            # If activation failed, log a warning. Input might go to the wrong window.
            # More robust solutions might involve platform-specific APIs (like pywinauto on Windows)
            # or retrying activation. For now, we proceed with a warning.
            active_title = active_window.title if active_window else "None"
            logging.warning(
                f"Window '{window_title}' might not be focused after activate(). "
                f"Actual active window: '{active_title}'. Input might be misdirected."
            )

        # --- Key Press Simulation ---
        logging.debug(f"Sending key press '{key_to_press}' via pydirectinput.")
        pydirectinput.press(key_to_press)
        # Pause briefly after the press, as defined in settings.
        time.sleep(KEY_PRESS_PAUSE)
        logging.info(f"Successfully sent key press '{key_to_press}' for button '{button}'.")

    except gw.PyGetWindowException as e:
        # Errors specifically related to pygetwindow operations (e.g., window closed unexpectedly).
        logging.error(f"PyGetWindow error interacting with '{window_title}': {e}")
    except Exception as e:
        # Catch other potential errors (e.g., from pydirectinput, time.sleep).
        logging.error(f"Unexpected error during input simulation for window '{window_title}': {e}")


# Example usage (for testing purposes)
# Note: The example usage below needs updating to work with the current
# function signature, which requires a valid window object.
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG) # Use DEBUG for detailed test output
    logging.info("--- Input Simulation Test ---")
    logging.info("Ensure the target emulator window (e.g., mGBA) is open.")
    time.sleep(2) # Pause to allow manual focus switching if needed.

    # --- Find the target window (replace 'mGBA' if needed) ---
    emulator_title_to_find = "mGBA"
    target_window = None
    try:
        windows = gw.getWindowsWithTitle(emulator_title_to_find)
        if windows:
            target_window = windows[0] # Use the first found window
            logging.info(f"Found target window: '{target_window.title}'")
        else:
            logging.error(f"Test failed: Could not find window with title '{emulator_title_to_find}'.")
    except Exception as find_err:
        logging.error(f"Error finding window: {find_err}")

    # --- Run tests only if window was found ---
    if target_window:
        test_buttons = ["A", "B", "UP", "DOWN", "LEFT", "RIGHT", "START", "SELECT", "L", "R", "InvalidButton"]

        for btn in test_buttons:
            logging.info(f"--- Testing button: '{btn}' ---")
            press_gba_button(target_window, btn)
            time.sleep(0.5) # Short pause between different button tests

        logging.info("--- Input simulation test finished ---")
    else:
        logging.warning("Skipping button press tests because the target window was not found.")