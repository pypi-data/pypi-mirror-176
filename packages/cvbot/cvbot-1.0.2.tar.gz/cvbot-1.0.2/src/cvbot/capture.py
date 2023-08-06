from images import Image
from cvbot.windows import get_window
from cvbot.screen import get_region 


dfwin = None

def default_window(wname):
    """
    str -> None
    Set 'dfwin' global variable to the window with title 'win'
    """
    global dfwin
    dfwin = get_window(wname)

def trim_pad(img):
    """
    npimage -> npimage
    Remove extra paddings in screenshot
    """
    return img[1:-8, 8:-8]

def capture_window(wname=""):
    """
    str -> Image | None
    Take a screenshot of a toplevel window and return it as an Image
    return None if not found
    """
    global dfwin
    win = None

    if wname == "":
        win = dfwin
    else:
        win = get_window(wname)
    
    if not (win is None):
        return Image(trim_pad(get_region(win.region)))


