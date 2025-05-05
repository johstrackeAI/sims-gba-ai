"""
Main entry point for the Sims GBA AI agent.

This script orchestrates the interaction between screen capture, OCR,
LLM decision-making, and input simulation to play The Sims Bustin' Out on GBA.
It continuously captures the emulator screen, analyzes the visual information,
gets a suggested action (button press) from an LLM, and executes that action.
It includes specific logic to handle potential game pauses by trying 'A'
and falling back to 'START' if 'A' doesn't appear to resume the game.
"""
import time
from sims_gba_ai.core.screen_capture import capture_emulator_window
from sims_gba_ai.core.llm_interaction import get_llm_suggestion
from sims_gba_ai.core.input_simulation import press_gba_button
from sims_gba_ai.core.ocr import extract_text_from_image # Added
from sims_gba_ai.config.settings import LOOP_DELAY
from sims_gba_ai.utils.window_utils import find_window # Changed import

def main_loop() -> None:
    """Runs the main control loop for the Sims GBA AI agent.

    This loop performs the following steps repeatedly:
    1. Finds the emulator window.
    2. Captures the current screen content of the emulator.
    3. Extracts text using OCR to understand the initial state.
    4. Sends the captured image to an LLM to get a suggested button press.
    5. Simulates the suggested button press.
    6. Includes special handling for the 'A' button, attempting 'START' as a
       fallback if 'A' doesn't seem to change the game state (e.g., unpause).
    7. Waits for a configured delay before the next iteration.

    The loop continues indefinitely until manually stopped or if the emulator
    window cannot be found initially.
    """
    print("Starting Sims GBA AI control loop...")
    emulator_title = "mGBA" # Target emulator window title
    print(f"Attempting to find emulator window: '{emulator_title}'")

    # Attempt to find the handle (hwnd) of the emulator window.
    hwnd = find_window(emulator_title)
    if not hwnd:
        # If the window is not found, the agent cannot function.
        print(f"Error: Emulator window '{emulator_title}' not found. Exiting.")
        return # Exit the application if the window isn't found.

    while True:
        print("\n--- New Loop Iteration ---")

        # --- Step 1: Capture and Analyze Current State ---
        print("Capturing emulator window...")
        initial_image = capture_emulator_window(hwnd)
        if not initial_image:
            print("Error: Failed to capture emulator window. Retrying...")
            # Consider adding logic to re-find hwnd if capture fails repeatedly.
            time.sleep(LOOP_DELAY)
            continue # Skip to the next iteration if capture failed.

        print("Extracting text via OCR...")
        initial_ocr_text = extract_text_from_image(initial_image)
        print(f"Initial OCR Text (first 50 chars): '{initial_ocr_text[:50]}'")

        # --- Step 2: Get LLM Suggestion ---
        print("Sending current state to LLM for action suggestion...")
        suggested_button = get_llm_suggestion(initial_image)

        if not suggested_button:
            print("Warning: LLM did not provide a valid button suggestion. Skipping action.")
            time.sleep(LOOP_DELAY)
            continue # Skip action if no valid suggestion received.

        print(f"LLM suggested button press: {suggested_button}")

        # --- Step 3: Simulate Input (with 'A' vs 'START' fallback) ---
        # Special handling for 'A' button: Often used for confirmation or interaction,
        # but sometimes the game might be paused, requiring 'START'.
        if suggested_button == 'A':
            print("LLM suggested 'A'. Executing 'A' and verifying state change...")
            press_gba_button(hwnd, 'A')
            print("Pressed 'A'.")
            time.sleep(0.5) # Brief pause to allow the screen to potentially update.

            # Verify if pressing 'A' changed the game state by re-capturing and comparing OCR text.
            print("Capturing screen again to check if 'A' was effective...")
            new_image = capture_emulator_window(hwnd)
            if not new_image:
                # If capture fails after pressing 'A', we can't verify.
                # As a fallback, assume 'A' might not have worked (e.g., game was paused)
                # and try pressing 'START' instead.
                print("Error: Failed to capture screen after pressing 'A'.")
                print("Fallback: Assuming 'A' was ineffective, trying 'START'...")
                press_gba_button(hwnd, 'START')
                print("Pressed 'START'.")
            else:
                print("Extracting text after 'A' press...")
                new_ocr_text = extract_text_from_image(new_image)
                print(f"New OCR Text (first 50 chars): '{new_ocr_text[:50]}'")

                # Compare OCR text before and after pressing 'A'.
                # If the text hasn't changed, 'A' likely didn't advance the game state
                # (e.g., the game might be paused). Try 'START' as a fallback.
                if new_ocr_text == initial_ocr_text:
                    print("OCR text unchanged after 'A'. Fallback: Trying 'START'...")
                    press_gba_button(hwnd, 'START')
                    print("Pressed 'START'.")
                else:
                    # If the text changed, assume 'A' was the correct action.
                    print("'A' press appears to have changed the game state. Proceeding.")

        else:
            # If the suggestion is not 'A', press the suggested button directly.
            print(f"Executing suggested button press: {suggested_button}")
            press_gba_button(hwnd, suggested_button)
            print(f"Pressed '{suggested_button}'.")

        # --- Step 4: Wait Before Next Cycle ---
        print(f"Waiting for {LOOP_DELAY} seconds before next loop iteration...")
        time.sleep(LOOP_DELAY)

if __name__ == "__main__":
    main_loop()