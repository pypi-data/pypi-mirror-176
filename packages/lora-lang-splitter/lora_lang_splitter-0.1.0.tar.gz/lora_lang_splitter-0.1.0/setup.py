# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lora_lang_splitter']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'lora-lang-splitter',
    'version': '0.1.0',
    'description': 'A package to split a text with both Chinese and English. Returns two separate Chinese and English strings.',
    'long_description': '# import\n\n`from lora_lang_splitter import split_eng_cn`\n\n# Usage\n\n`english_text, chinese_text = split_eng_cn("Markov\'s long 中文 text")`\n\n# Output\n\n`str(english_text), str(chinese_text)`\n',
    'author': 'Adrian-Wong',
    'author_email': 'adrian@asklora.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
