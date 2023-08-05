# ooo-dev-tools-gui-win

This package contains Automation for use with LIbreOffice and [OOO Development Tools] project.

## Installation

```sh
pip install ooo-dev-tools-gui-win
```

## DrawDispatcher Class

Contains methods for automatically adding Special Shapes to Draw.
This is done via GUI Automation.
Otherwise there is no other way to automatically add these shapes to Draw.

See Also:

- [OOO Development Tools - Part 3: Draw & Impress](https://python-ooo-dev-tools.readthedocs.io/en/latest/odev/part3/index.html)
- [Draw.add_dispatch_shape()](https://python-ooo-dev-tools.readthedocs.io/en/latest/src/office/draw.html#ooodev.office.draw.Draw.add_dispatch_shape)

![Callout_clouds](https://user-images.githubusercontent.com/4193389/200589660-9ccede18-b0b5-4052-a36c-ef3f5002ea7c.png)

This code adds the cloud seen above to a Draw page.

```python
from ooodev.office.draw import Draw, DrawingBitmapKind, ShapeDispatchKind
from ooodev.utils.lo import Lo
from ooodev.utils.gui import GUI
from odevgui_win.draw_dispatcher import DrawDispatcher

def main() -> int:
    loader = Lo.load_office(Lo.ConnectPipe())

    try:
        doc = Draw.create_draw_doc(loader)
        slide = Draw.get_slide(doc=doc, idx=0)

        GUI.set_visible(is_visible=True, odoc=doc)
        Lo.delay(1_000)
        GUI.zoom(view=GUI.ZoomEnum.ENTIRE_PAGE)

        shape = Draw.add_dispatch_shape(
            slide=slide,
            shape_dispatch=ShapeDispatchKind.CALLOUT_SHAPES_CLOUD_CALLOUT,
            x=140,
            y=60,
            width=50,
            height=30,
            fn=DrawDispatcher.create_dispatch_shape_win,
        )
        Draw.set_bitmap_color(shape, DrawingBitmapKind.LITTLE_CLOUDS)
    except Exception:
        Lo.close_office()
        raise
    return 0

if __name__ == "__main__":
    SystemExit(main())
```

## DialogAuto Class

Provides method for automatically handling dialog boxes.

See [Impress append Slides to existing slide show] example for a demonstration.

[OOO Development Tools]: https://python-ooo-dev-tools.readthedocs.io/en/latest/index.html
[Impress append Slides to existing slide show]: https://github.com/Amourspirit/python-ooouno-ex/tree/main/ex/auto/impress/odev_append_slides
