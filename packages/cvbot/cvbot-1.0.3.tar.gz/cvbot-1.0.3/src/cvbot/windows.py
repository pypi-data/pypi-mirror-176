from win32gui import FindWindowEx as find_window
from win32gui import GetWindowRect as get_window_pnts
from win32gui import IsWindowVisible, GetWindowText, EnumWindows, MoveWindow


lhwnd = None

class Window:
    def __init__(self, hwnd):
        self.hwnd = hwnd

    def resize(self, w, h):
        """
        self, int, int -> None
        Change window width and height to w, h
        """
        resize_window(self.hwnd, w, h)

    @property
    def region(self):
        """
        self -> tuple(int, int, int, int)
        Return the current region occupied by Window
               or (0, 0, 1, 1) if the window region couldn't be found
        """
        return get_window_region(self.hwnd)

def resize_window(hwnd, w, h):
    """
    String, int, int -> None
    Resize window with handle hwnd
    """
    global lhwnd
    lhwnd = hwnd

    if hwnd != 0:
        x, y = win_pos(hwnd)
        MoveWindow(hwnd, x, y, w, h, True)
    else:
        print("[Error] Couldn't find" +\
              " window with handle({})".format(hwnd))

def get_last_win():
    """
    None -> Window
    Return the last used window handle as a Window
    """
    global lhwnd

    return Window(lhwnd)

def get_active_wins():
    """
    None -> dict(str:binary)
    Return a dictionary of all active windows - key   : window name
                                                value : window handle
    """
    wins = {}

    def winEnumHandler(hwnd, ctx):
        nonlocal wins

        if IsWindowVisible(hwnd):
            name = GetWindowText(hwnd)
            wins[name] = hwnd 


    EnumWindows(winEnumHandler, None)
    return wins

def get_window(win):
    """
    str -> Window | None
    Find and return the window with name 'win'
    or return None if not found
    """
    global lhwnd
    hwnd = find_window(None, None, None, win)
    lhwnd = hwnd

    if hwnd != 0:
        return Window(hwnd)
    
def get_window_region(win, exact=False):
    """
    str | int -> Rect
    Find current running window
    by name and return window
    region on screen
    """
    global lhwnd
    if type(win) is str:
        hwnd = find_window(None, None, None, win)
    else:
        hwnd = win 
    lhwnd = hwnd

    if hwnd != 0:
        wnpnts = get_window_pnts(hwnd)
        return (wnpnts[0], wnpnts[1], wnpnts[2] - wnpnts[0],
                wnpnts[3] - wnpnts[1])
    else:
        if not exact:
            awins = get_active_wins()
            for awname in awins.keys():
                if awname != "" and win in awname:
                    return get_window_region(awname, True)
        print("[Error] Couldn't find" +\
              " window with name({})".format(win))
        return (0, 0, 1, 1)

def win_pos(hwnd):
    """
    binary -> int, int
    Given window handle return window top-left coordinates(x, y)
    """
    return get_window_pnts(hwnd)[0:2]
