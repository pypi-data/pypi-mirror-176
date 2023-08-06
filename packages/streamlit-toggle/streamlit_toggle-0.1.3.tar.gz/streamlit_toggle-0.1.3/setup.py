# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['streamlit_toggle']

package_data = \
{'': ['*']}

install_requires = \
['streamlit-space>=0.1.5,<0.2.0', 'streamlit>=1.14.0,<2.0.0']

setup_kwargs = {
    'name': 'streamlit-toggle',
    'version': '0.1.3',
    'description': 'Toggling component for Streamlit',
    'long_description': "# Streamlit Toggle\n\n[![Open in Streamlit][share_badge]][share_link] [![GitHub][github_badge]][github_link] [![PyPI][pypi_badge]][pypi_link] \n\nAdd toggle switches to your Streamlit app.\n\n\n\n## Installation\n\n```bash\npip install streamlit-toggle\n```\n\n\n\n## Quickstart\n\n```python\nimport streamlit as st\nfrom streamlit_toggle import toggle\n\nst.title('Streamlit Toggle')\ntoggle()\n```\n\n\n\n## License\n\nStreamlit Toggle has an MIT license, as found in the [LICENSE](https://github.com/imyizhang/streamlit-toggle/blob/main/LICENSE) file.\n\n\n\n## Documentation\n\n### streamlit_toggle.toggle\n\n#### `streamlit_toggle.toggle(container=None, widget='slider', label='', value=False, key=None, help=None, on_change=None, args=None, kwargs=None, *, disabled=False)`\n\nAdd a toggle switch to Streamlit app.\n\n**Parameters:**\n\n* **container** (any, optional): The Streamlit container. Defaults to `None`.\n* **widget** (str, optional): The input widget. Defaults to `'slider'`.\n* **label** (str, optional): The short label explaining what the toggle switch is for. Defaults to `''`.\n* **value** (bool, optional): The preselected value on first renders. Defaults to `False`.\n* **key** (str, optional): The unique key for the widget. Defaults to `None`, a key will be automatically generated.\n* **help** (str, optional): The tooltip that gets displayed next to the toggle switch. Defaults to `None`.\n* **on_change** (callable, optional): The callback invoked when the value of the toggle switch changes. Defaults to `None`.\n* **args** (tuple, optional): The tuple of args to pass to the callback. Defaults to `None`.\n* **kwargs** (dict, optional): The dictionary of kwargs to pass to the callback. Defaults to `None`.\n* **disabled** (bool, optional, keyword-only): Whether the toggle switch is to be disabled. Defaults to `False`.\n\n**Returns:**\n\n(bool): The value of the toggle switch.\n\n\n\n### streamlit_toggle.theme\n\n#### `streamlit_toggle.theme(container=None, widget='checkbox', label='Dark', value=False, key=None, help=None, *, disabled=False, path=None)`\n\nAdd a Streamlit Light and Dark theme toggle switch to Streamlit app.\n\n**Parameters:**\n\n* **container** (any, optional): The Streamlit container. Defaults to `None`.\n* **widget** (str, optional): The input widget. Defaults to `'checkbox'`.\n* **label** (str, optional): The short label explaining what the toggle switch is for. Defaults to `'Dark'`.\n* **value** (bool, optional): The preselected value on first renders. Defaults to `False`, the default Streamlit Light theme.\n* **key** (str, optional): The unique key for the widget. Defaults to `None`, a key will be automatically generated.\n* **help** (str, optional): The tooltip that gets displayed next to the toggle switch. Defaults to `None`.\n* **disabled** (bool, optional, keyword-only): Whether the toggle switch is to be disabled. Defaults to `False`.\n* **path** (str, optional, keyword-only): The path of Stramlit app. Defaults to `None`, the file path of the caller.\n\n**Returns:**\n\n(bool): The value of the toggle switch.\n\n\n\n## Contribution\n\n\n\n## Changelog\n\nVersion 0.1.0:\n\n* Made toggling component functional\n* Made essential theming component functional, toggling between Streamlit Light and Dark theme\n\n\n\n[share_badge]: https://static.streamlit.io/badges/streamlit_badge_black_white.svg\n[share_link]: https://share.streamlit.io/imyizhang/streamlit-toggle/main/streamlit_app.py\n\n[github_badge]: https://badgen.net/badge/icon/GitHub?icon=github&color=black&label\n[github_link]: https://github.com/imyizhang/streamlit-toggle\n\n[pypi_badge]: https://badgen.net/pypi/v/streamlit-toggle?icon=pypi&color=black&label\n[pypi_link]: https://www.pypi.org/project/streamlit-toggle",
    'author': 'Yi Zhang',
    'author_email': 'yizhang.dev@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://st-toggle.streamlit.app',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7, !=2.7.*, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*',
}


setup(**setup_kwargs)
