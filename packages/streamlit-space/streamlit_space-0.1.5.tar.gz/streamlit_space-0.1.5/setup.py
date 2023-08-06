# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['streamlit_space']

package_data = \
{'': ['*']}

install_requires = \
['streamlit>=1.14.0,<2.0.0']

setup_kwargs = {
    'name': 'streamlit-space',
    'version': '0.1.5',
    'description': 'Spacing component for Streamlit',
    'long_description': "# Streamlit Space\n\n[![Open in Streamlit][share_badge]][share_link] [![GitHub][github_badge]][github_link] [![PyPI][pypi_badge]][pypi_link] \n\nAdd blank lines to your Streamlit app.\n\n\n\n## Installation\n\n```bash\npip install streamlit-space\n```\n\n\n\n## Quickstart\n\n```python\nimport streamlit as st\nfrom streamlit_space import space\n\nst.title('Streamlit Space')\nspace()\n```\n\n\n\n## License\n\nStreamlit Space has an MIT license, as found in the [LICENSE](https://github.com/imyizhang/streamlit-space/blob/main/LICENSE) file.\n\n\n\n## Documentation\n\n### streamlit_space.space\n\n#### `streamlit_space.space(container=None, lines=1)`\n\nAdd blank lines to Streamlit app.\n\n**Parameters**:\n\n* **container** (any, optional): The Streamlit container. Defaults to `None`.\n* **lines** (int, optional): The number of blank lines to be added. Defaults to `1`.\n\n\n\n## Contribution\n\n\n\n## Changelog\n\nVersion 0.1.0:\n\n* Made spacing component functional\n\n\n\n[share_badge]: https://static.streamlit.io/badges/streamlit_badge_black_white.svg\n[share_link]: https://share.streamlit.io/imyizhang/streamlit-space/main/streamlit_app.py\n\n[github_badge]: https://badgen.net/badge/icon/GitHub?icon=github&color=black&label\n[github_link]: https://github.com/imyizhang/streamlit-space\n\n[pypi_badge]: https://badgen.net/pypi/v/streamlit-space?icon=pypi&color=black&label\n[pypi_link]: https://www.pypi.org/project/streamlit-space",
    'author': 'Yi Zhang',
    'author_email': 'yizhang.dev@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://st-space.streamlit.app',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7, !=2.7.*, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*',
}


setup(**setup_kwargs)
