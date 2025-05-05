import time
from sims_gba_ai.core.screen_capture import capture_emulator_window
from sims_gba_ai.core.llm_interaction import get_llm_suggestion
from sims_gba_ai.core.input_simulation import press_gba_button
from sims_gba_ai.config.settings import LOOP_DELAY

def main_loop():
    """
    Main control loop for the Sims GBA AI.
    Captures the screen, gets LLM suggestion, and simulates input.
    """
    print("Starting Sims GBA AI control loop...")
    while True:
        print("\n--- New Loop Iteration ---")
        
        # 1. Capture emulator window
        image = capture_emulator_window()

        if image:
            print("Emulator window captured successfully. Sending to LLM...")
            
            # 2. Get LLM suggestion
            suggested_button = get_llm_suggestion(image)

            if suggested_button:
                print(f"LLM suggested button: {suggested_button}")
                
                # 3. Simulate button press
                press_gba_button(suggested_button)
                print(f"Simulated pressing: {suggested_button}")
            else:
                print("LLM did not provide a valid button suggestion.")
        else:
            print("Error: Failed to capture emulator window. Is it running with the correct title?")

        # 4. Wait before next iteration
        print(f"Waiting for {LOOP_DELAY} seconds...")
        time.sleep(LOOP_DELAY)

if __name__ == "__main__":
    main_loop()