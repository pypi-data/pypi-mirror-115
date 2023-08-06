# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ikea_api',
 'ikea_api.endpoints',
 'ikea_api.endpoints.cart',
 'ikea_api.endpoints.item',
 'ikea_api.endpoints.order_capture',
 'ikea_api.endpoints.purchases']

package_data = \
{'': ['*']}

install_requires = \
['Brotli>=1.0.9,<2.0.0',
 'aiohttp>=3.7.4,<4.0.0',
 'chromedriver-autoinstaller>=0.2.2,<0.3.0',
 'requests>=2.25.0',
 'selenium>=3.141.0,<4.0.0']

setup_kwargs = {
    'name': 'ikea-api',
    'version': '0.5.1',
    'description': 'IKEA API Client',
    'long_description': 'Client for several IKEA APIs.\n\n[![License](https://img.shields.io/pypi/l/ikea_api?color=green)](https://github.com/vrslev/ikea-api-client/blob/master/LICENSE)\n[![Version](https://img.shields.io/pypi/v/ikea_api?color=green&label=version)](https://pypi.org/project/ikea_api/)\n[![Python Version](https://img.shields.io/pypi/pyversions/ikea_api?color=green)](https://pypi.org/project/ikea_api/)\n[![Downloads](https://img.shields.io/pypi/dm/ikea_api?color=green)](https://pypi.org/project/ikea_api/)\n\n# Features\n\n- Authorization (as guest or as user)\n- Manage Cart\n- Check available Delivery Services\n- Retrieve Purchases History and information about specific order\n- Fetch Product information\n\n# Installation\n\n```bash\npip install ikea_api\n```\n\nIf you are planning to use log in as registered user, you need to install Selenium and chromedriver:\n\n```bash\npip install ikea_api[driver]\n```\n\n# Initialization\n\n```python\nfrom ikea_api import IkeaApi\n\napi = IkeaApi(\n    token=...,  # If you already have a token and stored it somewhere\n    country_code="ru",\n    language_code="ru",\n)\n```\n\n# Endpoints\n\n## [Authorization](https://github.com/vrslev/ikea-api-client/blob/master/src/ikea_api/auth.py)\n\n### [As Guest](https://github.com/vrslev/ikea-api-client/blob/03c1add4fd03fc41a7fef41c35bd2aa9c0c36d4b/src/ikea_api/auth.py#L35-L35)\n\n```python\napi.login_as_guest()\n```\n\nFirst time you open IKEA.com guest token is being generated and stored in Cookies. It expires in 30 days.\n\n### [As Registered User](https://github.com/vrslev/ikea-api-client/blob/03c1add4fd03fc41a7fef41c35bd2aa9c0c36d4b/src/ikea_api/auth.py#L56-L56)\n\nToken lasts 1 day. It may take a while to get authorized token because of Selenium usage.\n\n```python\napi.login(username=..., password=...)\n```\n\n## [Cart](https://github.com/vrslev/ikea-api-client/blob/master/src/ikea_api/endpoints/cart/__init__.py)\n\nThis API endpoint allows you to do everything you would be able to do on the site, and even more:\n\n- Add, Delete and Update items\n- Show cart\n- Clear cart\n- Set and Delete Coupon\n- Copy cart from another user\n\nWorks with and without authorization. If you logged in all changes apply to the _real_ cart. Use case: programmatically add items to cart and order it manually on IKEA.com.\n\nExample:\n\n```python\ncart = api.Cart\ncart.add_items({"30457903": 1})\nprint(cart.show())\n```\n\n## [Order Capture](https://github.com/vrslev/ikea-api-client/blob/master/src/ikea_api/endpoints/order_capture/__init__.py)\n\nCheck availability for Pickup or Delivery. This is the only way.\n\nIf you need to know whether items are available in stores, check out [ikea-availability-checker](https://github.com/Ephigenia/ikea-availability-checker).\n\n```python\napi.OrderCapture(zip_code="101000")\n```\n\n## [Purchases](https://github.com/vrslev/ikea-api-client/blob/master/src/ikea_api/endpoints/purchases/__init__.py)\n\n### [Order History](https://github.com/vrslev/ikea-api-client/blob/fc264640ca1f27f4a58c1c57891a917414518a7d/src/ikea_api/endpoints/purchases/__init__.py#L34-L34)\n\n```python\napi.login(username=..., password=...)\nhistory = api.Purchases.history()\n```\n\n### [Order Info](https://github.com/vrslev/ikea-api-client/blob/fc264640ca1f27f4a58c1c57891a917414518a7d/src/ikea_api/endpoints/purchases/__init__.py#L44-L44)\n\n```python\napi.login(username=..., password=...)\norder = api.Purchases.order_info(order_number=...)\n\n# Or use it without authorization, email is required\napi.login_as_guest()\norder = api.order_info(order_number=..., email=...)\n```\n\n## [Item Specs](https://github.com/vrslev/ikea-api-client/tree/master/src/ikea_api/endpoints/item)\n\nGet information about item by item number\n\n```python\nitem_codes = ["30457903"]\n\nitems = api.fetch_items_specs.iows(item_codes)\n\n# or\nitems = api.fetch_items_specs.ingka(item_codes)\n\n# or\nitem_codes_dict = {d: True for d in items}  # True — is SPR i. e. combination\nitems = api.fetch_items_specs.pip(item_codes_dict)\n```\n\nThere are many ways because information about some items is not available in some endpoints.\n\n# Response Examples\n\nYou can review response examples for all endpoint before using it [here](https://github.com/vrslev/ikea-api-client/tree/master/response_examples)\n',
    'author': 'vrslev',
    'author_email': 'mail@vrslev.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vrslev/ikea-api-client',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
