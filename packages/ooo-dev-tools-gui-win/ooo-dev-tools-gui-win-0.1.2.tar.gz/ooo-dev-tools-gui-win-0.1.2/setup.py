# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['odevgui_win']

package_data = \
{'': ['*']}

install_requires = \
['ooo-dev-tools>=0.6.0', 'pywinauto>=0.6.8']

setup_kwargs = {
    'name': 'ooo-dev-tools-gui-win',
    'version': '0.1.2',
    'description': 'Methods for ooo-dev-tools and LibreOffice that require automatic GUI interaction for windows.',
    'long_description': '# ooo-dev-tools-gui-win\n\nThis package contains Automation for use with LIbreOffice and [OOO Development Tools] project.\n\n## Installation\n\n```sh\npip install ooo-dev-tools-gui-win\n```\n\n## DrawDispatcher Class\n\nContains methods for automatically adding Special Shapes to Draw.\nThis is done via GUI Automation.\nOtherwise there is no other way to automatically add these shapes to Draw.\n\nSee Also:\n\n- [OOO Development Tools - Part 3: Draw & Impress](https://python-ooo-dev-tools.readthedocs.io/en/latest/odev/part3/index.html)\n- [Draw.add_dispatch_shape()](https://python-ooo-dev-tools.readthedocs.io/en/latest/src/office/draw.html#ooodev.office.draw.Draw.add_dispatch_shape)\n\n![Callout_clouds](https://user-images.githubusercontent.com/4193389/200589660-9ccede18-b0b5-4052-a36c-ef3f5002ea7c.png)\n\nThis code adds the cloud seen above to a Draw page.\n\n```python\nfrom ooodev.office.draw import Draw, DrawingBitmapKind, ShapeDispatchKind\nfrom ooodev.utils.lo import Lo\nfrom ooodev.utils.gui import GUI\nfrom odevgui_win.draw_dispatcher import DrawDispatcher\n\ndef main() -> int:\n    loader = Lo.load_office(Lo.ConnectPipe())\n\n    try:\n        doc = Draw.create_draw_doc(loader)\n        slide = Draw.get_slide(doc=doc, idx=0)\n\n        GUI.set_visible(is_visible=True, odoc=doc)\n        Lo.delay(1_000)\n        GUI.zoom(view=GUI.ZoomEnum.ENTIRE_PAGE)\n\n        shape = Draw.add_dispatch_shape(\n            slide=slide,\n            shape_dispatch=ShapeDispatchKind.CALLOUT_SHAPES_CLOUD_CALLOUT,\n            x=140,\n            y=60,\n            width=50,\n            height=30,\n            fn=DrawDispatcher.create_dispatch_shape_win,\n        )\n        Draw.set_bitmap_color(shape, DrawingBitmapKind.LITTLE_CLOUDS)\n    except Exception:\n        Lo.close_office()\n        raise\n    return 0\n\nif __name__ == "__main__":\n    SystemExit(main())\n```\n\n## DialogAuto Class\n\nProvides method for automatically handling dialog boxes.\n\nSee [Impress append Slides to existing slide show] example for a demonstration.\n\n[OOO Development Tools]: https://python-ooo-dev-tools.readthedocs.io/en/latest/index.html\n[Impress append Slides to existing slide show]: https://github.com/Amourspirit/python-ooouno-ex/tree/main/ex/auto/impress/odev_append_slides\n',
    'author': ':Barry-Thomas-Paul: Moss',
    'author_email': 'vibrationoflife@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Amourspirit/python-ooo-dev-tools-gui-win',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
