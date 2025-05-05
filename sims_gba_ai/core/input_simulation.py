import pydirectinput
import time
import pygetwindow as gw
import logging

from sims_gba_ai.utils.window_utils import find_window
from sims_gba_ai.config.settings import EMULATOR_WINDOW_TITLE, GBA_KEY_MAPPINGS, KEY_PRESS_PAUSE

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def press_gba_button(button: str):
    """
    Simulates pressing a GBA button by mapping it to a keyboard key and sending the input
    to the specified emulator window.

    Args:
        button: The GBA button to press (e.g., "Up", "A"). Must be a key in GBA_KEY_MAPPINGS.
    """
    if button not in GBA_KEY_MAPPINGS:
        logging.error(f"Invalid GBA button: '{button}'. Not found in key mappings.")
        return

    key_to_press = GBA_KEY_MAPPINGS[button]
    logging.info(f"Attempting to press GBA button '{button}' (mapped to key '{key_to_press}')")

    emulator_window = find_window(EMULATOR_WINDOW_TITLE)

    if emulator_window:
        try:
            # Attempt to focus the window
            if emulator_window.isMinimized:
                emulator_window.restore()
            # Sometimes activate() might not be enough or might fail if the window isn't cooperative
            # Bringing to front can be more reliable on some systems
            emulator_window.activate() # Tries to activate
            time.sleep(0.1) # Short pause to allow focus to shift

            # Double-check if activation worked (optional, but can be useful)
            active_window = gw.getActiveWindow()
            if active_window is None or active_window.title != EMULATOR_WINDOW_TITLE:
                 # Fallback or more forceful focus attempt if needed, e.g., using pywinauto if on Windows
                 # For now, we'll just log a warning if activation might have failed
                 logging.warning(f"Emulator window '{EMULATOR_WINDOW_TITLE}' might not be focused. Sending key press anyway.")
                 # You might need more robust focus handling depending on the OS and emulator

            logging.info(f"Sending key press '{key_to_press}' to window '{EMULATOR_WINDOW_TITLE}'")
            pydirectinput.press(key_to_press)
            time.sleep(KEY_PRESS_PAUSE) # Pause after pressing the key
            logging.info(f"Key press '{key_to_press}' sent and paused.")

        except gw.PyGetWindowException as e:
            logging.error(f"Error interacting with emulator window '{EMULATOR_WINDOW_TITLE}': {e}")
        except Exception as e:
            # Catch other potential errors during activation or key press
            logging.error(f"An unexpected error occurred during input simulation: {e}")
    else:
        logging.error(f"Emulator window with title '{EMULATOR_WINDOW_TITLE}' not found.")

# Example usage (for testing purposes)
if __name__ == '__main__':
    logging.info("Starting input simulation test...")
    # Make sure the emulator window is open before running this test
    time.sleep(2) # Give time to switch to the emulator window manually if needed

    test_buttons = ["A", "B", "Start", "Invalid"]

    for btn in test_buttons:
        print(f"\nTesting button: {btn}")
        press_gba_button(btn)
        time.sleep(1) # Pause between test presses

    logging.info("Input simulation test finished.")