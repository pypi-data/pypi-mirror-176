from __future__ import annotations
from typing import List

import uno
from com.sun.star.drawing import XShape
from com.sun.star.drawing import XDrawPage

from ooodev.utils.data_type.window_title import WindowTitle
from ooodev.utils.lo import Lo
from ooodev.office.draw import Draw

import pywinauto
from pywinauto.application import Application
from pywinauto.keyboard import send_keys


class DrawDispatcher:
    """Draw Dispat Automation"""

    @staticmethod
    def create_dispatch_shape(slide: XDrawPage, shape_dispatch: str, *titles: WindowTitle) -> XShape | None:
        """
        Creates a dispatch shape in two steps.

        1. Select the shape by calling ``Lo.dispatch_cmd()``
        2. Creates the shape on screen by imitating a press and drag on the visible page.

        A reference to the created shape is obtained by assuming that it's the new
        top-most element on the page.

        Args:
            slide (XDrawPage): Draw Page
            shape_dispatch (str): Shape Dispatch Command
            *titles: Optional Extended sequence of title information. This is used to match windows title.

        Returns:
            XShape | None: Shape on Success; Otherwise, ``None``.

        Notes:
            Assumes that connection to LibreOffice has been made with ``Lo.load_office()``
        """
        num_shapes = slide.getCount()

        # select the shape icon; Office must be visible
        Lo.dispatch_cmd(shape_dispatch)
        # wait just a sec.
        # Lo.delay(1_000)

        # Untitled 1 - LibreOffice Impress
        # ahk_class SALFRAME
        # ahk_exe soffice.bin

        # click and drag on the page to create the shape on the page;
        # the current page must be visible
        lst_titles: List[WindowTitle] = list(titles)
        if len(lst_titles) == 0:
            lst_titles.append(WindowTitle(".*LibreOffice Draw", True))
            lst_titles.append(WindowTitle(".*LibreOffice Impress", True))

        app = None
        title_arg = None
        for title in lst_titles:
            d_args = {"class_name": title.class_name}
            if title.is_regex:
                d_args["title_re"] = title.title
            else:
                d_args["title"] = title.title
            try:
                app = Application().connect(**d_args)
                title_arg = title
                if app:
                    break
            except pywinauto.ElementNotFoundError:
                app = None
        if app is None:
            raise pywinauto.ElementNotFoundError()
        if title_arg.is_regex:
            win = app.window(title_re=title_arg.title)
        else:
            win = app.window(title=title_arg.title)

        win.set_focus()
        Lo.delay(500)
        rect = win.rectangle()
        center_x = round((rect.right - rect.left) / 2) + rect.left
        center_y = round((rect.bottom - rect.top) / 2) + rect.top

        pywinauto.mouse.press(button="left", coords=(center_x, center_y))
        pywinauto.mouse.release(button="left", coords=(center_x + 50, center_y + 50))

        # get a reference to the shape by assuming it's the top one on the page
        Lo.delay(300)
        num_shapes2 = slide.getCount()
        shape = None
        if num_shapes2 == num_shapes + 1:
            Lo.print(f'Shape "{shape_dispatch}" created')
            shape = Draw.find_top_shape(slide)
        else:
            Lo.print(f'Shape "{shape_dispatch}" NOT created')

        # escape deselects the shape that was just created.
        # this is critial in cases where one shape is drawn on top of another.
        send_keys("{VK_ESCAPE}")
        return shape
