import pygetwindow as gw
import warnings

def find_window(title: str):
    """
    Finds a window by its title.

    Args:
        title: The exact title of the window to find.

    Returns:
        The window object if found, otherwise None.
    """
    windows = gw.getWindowsWithTitle(title)
    if windows:
        return windows[0] # Return the first match
    else:
        warnings.warn(f"Window with title '{title}' not found.")
        return None