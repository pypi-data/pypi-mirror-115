# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['systa',
 'systa.backend',
 'systa.events',
 'systa.events.decorators',
 'systa.experimental',
 'systa.experimental.decorators',
 'systa.scripts']

package_data = \
{'': ['*']}

install_requires = \
['boltons>=21.0.0,<22.0.0',
 'pynput>=1.7.3,<2.0.0',
 'pywin32>=301,<302',
 'typeguard>=2.12.0,<3.0.0',
 'typing-inspect>=0.7.1,<0.8.0']

setup_kwargs = {
    'name': 'systa',
    'version': '0.2.0',
    'description': 'Windows GUI automation with a cool API.',
    'long_description': 'Systa: A ``Window`` for `windows <https://en.wikipedia.org/wiki/Window_(computing)>`_ on `Windows™ <https://en.wikipedia.org/wiki/Microsoft_Windows>`_.\n==========================================================================================================================================================\n\n**Systa** is a Microsoft Windows automation library, built for people who aren\'t Microsoft\nWindows programming gurus.\n\n`Documentation. <https://dmwyatt.github.io/systa/>`_\n\nInstall\n-------\n\n``pip install systa``\n\nBasic Usage\n-----------\n\n>>> from systa.windows import current_windows\n>>> "Untitled - Notepad" in current_windows\nTrue\n>>> "🍔" in current_windows\nFalse\n>>> notepad = current_windows["Untitled - Notepad"][0]\n>>> notepad.maximized\nFalse\n>>> notepad.maximized = True # it\'s now maximized\n>>> notepad.maximized\nTrue\n\nEvents\n------\nThe real power of systa springs from its integration with Windows system hooks.  You can\nrun code when things happen on the system.\n\n.. code-block:: python\n\n  from systa.events.decorators import listen_to, filter_by\n  from systa.events.store import callback_store\n  from systa.events.types import EventData\n\n  @filter_by.require_size_is_less_than(200, 200)\n  @filter_by.require_title("*Notepad")\n  @listen_to.restore\n  @listen_to.create\n  def a_func_to_do_the_thing(event_data: EventData):\n      print(f"Notepad restored or created! ({event_data.window.width}, {event_data.window.height})")\n\n  callback_store.run()\n\nThe above code prints a message when:\n\n1. A window is opened ``OR`` a window is restored from a minimized state.\n2. ``AND`` the window\'s title ends with the string ``Notepad``.\n3. ``AND`` the window\'s size is less than 200x200.\n',
    'author': 'Dustin Wyatt',
    'author_email': 'dustin.wyatt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dmwyatt/systa',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
