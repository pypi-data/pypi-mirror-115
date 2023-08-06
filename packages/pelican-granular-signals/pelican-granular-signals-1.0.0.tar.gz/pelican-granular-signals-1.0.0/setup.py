# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pelican', 'pelican.plugins.granular_signals']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pelican-granular-signals',
    'version': '1.0.0',
    'description': 'Add more granular signals to Pelican.',
    'long_description': '..  This file is part of the pelican-granular-signals plugin.\n..  Copyright 2021 Kurt McKee <contactme@kurtmckee.org>\n..  Released under the MIT license.\n\npelican-granular-signals\n************************\n\n*Ensure that your Pelican plugin is called at the right time, every time.*\n\n----\n\nLove `Pelican`_ but hate that your finalization plugin isn\'t always called in the right order?\nDon\'t let your plugin get lost in the shuffle of the ``finalized`` signal!\n**pelican-granular-signals** adds new finalization signals\nthat guarantee your plugin is called at the right time, every time.\n\n\n\nNew Pelican signals\n===================\n\nWhen **pelican-granular-signals** is installed,\nthe following signals will be called immediately after the ``finalized`` signal:\n\n*   ``sitemap``\n*   ``optimize``\n*   ``minify``\n*   ``compress``\n*   ``deploy``\n\nEach signal will be sent with the same argument that is sent to the ``finalized`` signal.\n\n\n\nConnecting to granular signals\n==============================\n\nYour plugin must register with `blinker`_ directly.\nHere\'s a complete example:\n\n..  code-block:: python\n\n    import blinker\n\n    import pelican.plugins.granular_signals\n\n\n    def register():\n        # This line is highly recommended so users\n        # don\'t have to update their configurations.\n        pelican.plugins.granular_signals.register()\n\n        # Connect your awesome plugin to a granular signal.\n        blinker.signal("deploy").connect(deploy_site)\n\n\n    # -----------------------------------------------------\n    # Put your awesome plugin code here.\n\n    import subprocess\n\n    def deploy_site(instance):\n        subprocess.run(instance.settings["DEPLOY_COMMAND"])\n\n\n\nHelping users out\n=================\n\nTo make life easier for users, consider taking these two steps:\n\n1.  List **pelican-granular-signals** as a dependency so it will be automatically installed with your plugin.\n2.  When Pelican calls your plugin\'s ``register()`` function, call ``pelican.plugins.granular_signals.register()``.\n\nPelican 4.5 introduced a new, automatic plugin loading feature\nand **pelican-granular-signals** is designed to work with this feature!\nUnfortunately, if a user specifies which plugins to load in their configuration file\nthen automatic plugin loading will be disabled.\nIt is therefore recommended that you call ``pelican.plugins.granular_signals.register()``\nin your plugin\'s ``register()`` function.\n\n``pelican.plugins.granular_signals.register()`` can be called multiple times without creating any problems.\n\n\n\n\n..  Links\n..  =====\n\n..  _Pelican: https://getpelican.com/\n..  _blinker: https://github.com/jek/blinker\n',
    'author': 'Kurt McKee',
    'author_email': 'contactme@kurtmckee.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
