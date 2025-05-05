import mss
import mss.tools
from PIL import Image
import numpy as np

from sims_gba_ai.utils.window_utils import find_window
from sims_gba_ai.config.settings import EMULATOR_WINDOW_TITLE

def capture_emulator_window():
    """
    Captures the content of the emulator window specified by EMULATOR_WINDOW_TITLE.

    Returns:
        A PIL.Image object containing the screenshot of the emulator window,
        or None if the window is not found.
    """
    window = find_window(EMULATOR_WINDOW_TITLE)
    if not window:
        return None

    # Define the bounding box dictionary for mss
    # window.box gives (left, top, right, bottom)
    # mss expects {'top': top, 'left': left, 'width': width, 'height': height}
    monitor = {
        "top": window.top,
        "left": window.left,
        "width": window.width,
        "height": window.height,
    }

    with mss.mss() as sct:
        # Grab the data
        sct_img = sct.grab(monitor)

        # Convert to PIL Image
        # The grab function returns BGRA, Pillow needs RGB
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        # Alternatively, using numpy for conversion:
        # img_np = np.array(sct_img)
        # img = Image.fromarray(img_np[:, :, :3]) # Drop alpha channel if present

        return img

if __name__ == '__main__':
    # Example usage: Capture and save the image
    img = capture_emulator_window()
    if img:
        img.save("emulator_capture.png")
        print("Emulator window captured and saved to emulator_capture.png")
    else:
        print(f"Could not find emulator window: {EMULATOR_WINDOW_TITLE}")