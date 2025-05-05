"""
Screen Capture Module.

Provides functionality to capture the screen content of a specific window,
typically an emulator window, using the `mss` library.
"""
import mss
import mss.tools
from PIL import Image
import numpy as np
from typing import Optional # Added for type hinting
# Note: pygetwindow is used for the type hint, but not directly imported
# to avoid dependency if only used for type checking.

# Removed find_window import as window object is passed in
# from sims_gba_ai.utils.window_utils import find_window
# Removed EMULATOR_WINDOW_TITLE import as it's no longer needed here
# from sims_gba_ai.config.settings import EMULATOR_WINDOW_TITLE

def capture_emulator_window(window: 'pygetwindow.Window') -> Optional[Image.Image]:
    """Captures the screen content of a specified window.

    Uses the `mss` library to take a screenshot of the area defined by the
    bounding box of the provided window object.

    Args:
        window: A window object (compatible with `pygetwindow.Window` interface,
                providing `top`, `left`, `width`, `height` attributes)
                representing the target window to capture.

    Returns:
        A PIL.Image object containing the screenshot in RGB format,
        or None if the window object is invalid or the capture fails.
    """
    if not window or not all(hasattr(window, attr) for attr in ['top', 'left', 'width', 'height']):
        print("Error: Invalid or incomplete window object passed to capture_emulator_window.")
        return None

    # Define the screen region to capture based on the window's coordinates.
    # `mss` requires a dictionary with 'top', 'left', 'width', and 'height'.
    monitor = {
        "top": window.top,
        "left": window.left,
        "width": window.width,
        "height": window.height,
    }

    try:
        with mss.mss() as sct:
            # Grab the image data for the specified monitor region.
            sct_img = sct.grab(monitor)

            # Convert the raw BGRA data from mss to an RGB PIL Image.
            # Pillow's frombytes expects RGB, so we specify "BGRX" to correctly
            # interpret the BGRA byte order and ignore the alpha channel.
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

            # Alternative numpy conversion (usually slightly slower):
            # img_np = np.array(sct_img) # Convert to numpy array (BGRA)
            # img_rgb = img_np[:, :, :3][:, :, ::-1] # Slice RGB, reverse BGR to RGB
            # img = Image.fromarray(img_rgb) # Convert numpy array to PIL Image

            return img
    except Exception as e:
        print(f"Error during screen capture: {e}")
        return None

# Note: The example usage below needs updating to work with the current
# function signature, which requires a valid window object.
# It might involve using find_window from utils or mocking a window object.
if __name__ == '__main__':
    # Example usage: Capture and save the image
    # This requires a valid 'window' object, e.g., from find_window()
    print("Note: Direct execution of this script requires modification to obtain a window object.")
    # Example placeholder:
    # from sims_gba_ai.utils.window_utils import find_window
    # emulator_title = "mGBA" # Or your emulator title
    # target_window = find_window(emulator_title)
    # if target_window:
    #     img = capture_emulator_window(target_window)
    #     if img:
    #         img.save("emulator_capture.png")
    #         print("Emulator window captured and saved to emulator_capture.png")
    #     else:
    #         print("Failed to capture the window content.")
    # else:
    #     print(f"Could not find emulator window: {emulator_title}")