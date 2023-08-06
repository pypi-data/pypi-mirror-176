# Streamlit Toggle

[![Open in Streamlit][share_badge]][share_link] [![GitHub][github_badge]][github_link] [![PyPI][pypi_badge]][pypi_link] 

Add toggle switches to your Streamlit app.



## Installation

```bash
pip install streamlit-toggle
```



## Quickstart

```python
import streamlit as st
from streamlit_toggle import toggle

st.title('Streamlit Toggle')
toggle()
```



## License

Streamlit Toggle has an MIT license, as found in the [LICENSE](https://github.com/imyizhang/streamlit-toggle/blob/main/LICENSE) file.



## Documentation

### streamlit_toggle.toggle

#### `streamlit_toggle.toggle(container=None, widget='slider', label='', value=False, key=None, help=None, on_change=None, args=None, kwargs=None, *, disabled=False)`

Add a toggle switch to Streamlit app.

**Parameters:**

* **container** (any, optional): The Streamlit container. Defaults to `None`.
* **widget** (str, optional): The input widget. Defaults to `'slider'`.
* **label** (str, optional): The short label explaining what the toggle switch is for. Defaults to `''`.
* **value** (bool, optional): The preselected value on first renders. Defaults to `False`.
* **key** (str, optional): The unique key for the widget. Defaults to `None`, a key will be automatically generated.
* **help** (str, optional): The tooltip that gets displayed next to the toggle switch. Defaults to `None`.
* **on_change** (callable, optional): The callback invoked when the value of the toggle switch changes. Defaults to `None`.
* **args** (tuple, optional): The tuple of args to pass to the callback. Defaults to `None`.
* **kwargs** (dict, optional): The dictionary of kwargs to pass to the callback. Defaults to `None`.
* **disabled** (bool, optional, keyword-only): Whether the toggle switch is to be disabled. Defaults to `False`.

**Returns:**

(bool): The value of the toggle switch.



### streamlit_toggle.theme

#### `streamlit_toggle.theme(container=None, widget='checkbox', label='Dark', value=False, key=None, help=None, *, disabled=False, path=None)`

Add a Streamlit Light and Dark theme toggle switch to Streamlit app.

**Parameters:**

* **container** (any, optional): The Streamlit container. Defaults to `None`.
* **widget** (str, optional): The input widget. Defaults to `'checkbox'`.
* **label** (str, optional): The short label explaining what the toggle switch is for. Defaults to `'Dark'`.
* **value** (bool, optional): The preselected value on first renders. Defaults to `False`, the default Streamlit Light theme.
* **key** (str, optional): The unique key for the widget. Defaults to `None`, a key will be automatically generated.
* **help** (str, optional): The tooltip that gets displayed next to the toggle switch. Defaults to `None`.
* **disabled** (bool, optional, keyword-only): Whether the toggle switch is to be disabled. Defaults to `False`.
* **path** (str, optional, keyword-only): The path of Stramlit app. Defaults to `None`, the file path of the caller.

**Returns:**

(bool): The value of the toggle switch.



## Contribution



## Changelog

Version 0.1.0:

* Made toggling component functional
* Made essential theming component functional, toggling between Streamlit Light and Dark theme



[share_badge]: https://static.streamlit.io/badges/streamlit_badge_black_white.svg
[share_link]: https://share.streamlit.io/imyizhang/streamlit-toggle/main/streamlit_app.py

[github_badge]: https://badgen.net/badge/icon/GitHub?icon=github&color=black&label
[github_link]: https://github.com/imyizhang/streamlit-toggle

[pypi_badge]: https://badgen.net/pypi/v/streamlit-toggle?icon=pypi&color=black&label
[pypi_link]: https://www.pypi.org/project/streamlit-toggle