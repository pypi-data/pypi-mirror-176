# /usr/bin/env python3

import fxcg


def getString(x: int, y: int) -> str:
    buffer: str = ""

    start: int = 0
    cursor: int = 0

    key: int = 0
    while True:
        key = GetKey()

        if key == KEY_CTRL_EXIT or key == KEY_CTRL_EXE:
            return buffer

        if key and key < 30000:
            buffer, cursor = EditMBStringChar(buffer, cursor, key)

            DisplayMBString("*" * min(len(buffer), 20), start, cursor, x, y)
        else:
            buffer, start, cursor, key = EditMBStringCtrl(buffer, key, x, y)


def handleTimer(num: int) -> None:
    # Simulate MENU press
    Keyboard_PutKeycode(0x04, 0x09, 0)

    # Stop timer and deinstall
    Timer_Stop(num)
    Timer_Deinstall(num)


Bdisp_EnableColor(0)
Bkey_SetAllFlags(0x80)
buf: str = ""

while True:
    # Clear screen
    Bdisp_AllClr_VRAM()

    # Disable menu return
    SetGetkeyToMainFunctionReturnFlag(False)

    # Turn off
    PowerOff(False)
    SetGetkeyToMainFunctionReturnFlag(False)

    # When on, print "Enter password: "
    PrintXY(1, 1, "Enter password:")

    # Search through user info
    password: str = None
    _, _, password = GetLatestUserInfo()

    # Get password entered
    buf = getString(1, 2)

    # If correct psasword
    if buf == password or password == None:
        # Enable menu return
        SetGetkeyToMainFunctionReturnFlag(True)

        # Install a timer to simulate MENU press
        if Timer_Install(lambda: handleTimer(6), 6) == -1:
            # If the timer cannot be installed, manually quit
            break

        # Start the MENU timer
        Timer_Start(6)

        # Let OS know we've 'pressed' MENU, but timeout as soon as we re-enter the program
        GetKeyWait_OS(2)
