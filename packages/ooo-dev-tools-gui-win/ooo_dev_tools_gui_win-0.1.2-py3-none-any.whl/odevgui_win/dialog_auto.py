from __future__ import annotations
import threading
import time
from typing import overload
import pywinauto
from pywinauto.application import Application
from pywinauto.keyboard import send_keys

# Confirmation
# ahk_class SALSUBFRAME
# ahk_exe soffice.bin


class DialogAuto:
    """Dialog Automation"""

    @overload
    @staticmethod
    def monitor_dialog(send_key: str) -> None:
        ...

    @overload
    @staticmethod
    def monitor_dialog(send_key: str, title: str) -> None:
        ...

    @overload
    @staticmethod
    def monitor_dialog(send_key: str, title: str, is_re_title: bool) -> None:
        ...

    @staticmethod
    def monitor_dialog(send_key: str, title: str = "Confirmation", is_re_title: bool = False) -> None:
        """
        Monitors for a dialog and press the button via its short cut keys such as ``alt+y``.

        Args:
            send_key (str): The key for the alt shortcut such as ``y`` or ``n`` or ``c``
            title (str, optional): The title of the dialog to monitor. Defaults to "Confirmation".
            is_re_title (bool, optional): Determines if the title is searched for as a regular expresson. Defaults to False.
        """
        # start thread
        x = threading.Thread(target=DialogAuto._confirmation, args=(send_key, title, is_re_title), daemon=True)
        x.start()

    @staticmethod
    def _confirmation(key: str, title: str, is_re_tile: bool) -> None:
        # connects to a LibreOffice Dialog such as a Confirmaton dialog.
        while 1:
            try:
                if is_re_tile:
                    app = Application().connect(title_re=title, class_name="SALSUBFRAME")
                else:
                    app = Application().connect(title=title, class_name="SALSUBFRAME")

            except pywinauto.ElementNotFoundError:
                pass
            else:
                send_keys("{VK_MENU down}" f"{key}" "{VK_MENU up}")
            time.sleep(0.7)
