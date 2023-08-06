# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['linenotify']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.3.0,<10.0.0',
 'opencv-python>=4.6.0.66,<5.0.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'linenotify-python',
    'version': '0.1.1',
    'description': 'LINE notify Web API wrapper',
    'long_description': '# linenotify-python\n\nLINE notify Web API wrapper\n\nPlenty of [internal validations](./linenotify/validations.py), easy [error handling](./linenotify/exceptions.py).\n\n## Install\n\n```\npip install linenotify-python\n```\n\n## Usage\n\n```python\nfrom os import environ, path\n\nimport cv2\nimport linenotify as ln\n\n\nTOKEN = environ[\'LINENOTIFY_TOKEN\']\n\n\n#\n# Standard usage\n# - Provides all the options described in the documentation.\n#\nservice = ln.Service(TOKEN)\n\nservice.notify("text")\nservice.notify("text + image", cv2.imread(path.join(path.dirname(__file__), "otaku.png")))\nservice.notify("text + sticker", (446, 1988))\nservice.notify("text + url", ("http://example.com/thumb.jpg", "https://example.com/body.jpeg"))\nservice.notify("without notification", notification_disabled=True)\n\n#\n# Check API status\n# - Status can be obtained from "status" and "notify".\n#\nstatus = service.status\nstatus = service.notify("text")\n\n#\n# Error handling\n# - All exceptions are derived from LINENotifyException, easily caught.\n#\ninvalid_service = ln.Service("invalid token")\ntry:\n    invalid_service.notify("raises an error")\n    invalid_service.notify("text + image", cv2.imread("very_large_image.png"))\n    invalid_service.notify("text + url", ("url_which_does_not_exist", "same_as_left"))\n    # and so on ...\n\nexcept ln.LINENotifyException:\n    pass\n```\n\n# API documents\n\n- [LINE Notify API Document](https://notify-bot.line.me/doc/en/)\n- [List of available stickers](https://developers.line.biz/en/docs/messaging-api/sticker-list/)\n',
    'author': 'Koutaro Mukai',
    'author_email': 'mukai.k1011k@outlook.jp',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mukai1011/linenotify-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
