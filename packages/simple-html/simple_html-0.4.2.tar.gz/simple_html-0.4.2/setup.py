# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simple_html']

package_data = \
{'': ['*']}

extras_require = \
{':python_version >= "3.7" and python_version < "3.8"': ['typed-ast==1.4.3']}

setup_kwargs = {
    'name': 'simple-html',
    'version': '0.4.2',
    'description': 'Template-less html rendering in Python',
    'long_description': '# simple_html\n\n### Template-less. Type-safe. Minified by default.\n\nsimple_html is built to simplify HTML rendering in Python. No templates needed. Just create HTML in \nnormal Python. In most cases, the code will be more concise than standard HTML. Other benefits include:\n- typically renders fewer bytes than template-based rendering\n- types mean your editor and tools can help you write correct code faster\n- no framework needed\n- lightweight\n\n\n### Installation\n`pip install simple_html`\n\n\n### Usage\n```python\nfrom simple_html.nodes import body, head, html, p\nfrom simple_html.render import render\n\nnode = html(\n    head,\n    body(\n        p.attrs(id="hello")( \n            "Hello World!"\n        )\n    )\n)\n\nrender(node)  # returns: <html><head></head><body><p id="hello">Hello World!</p></body></html> \n```\n\n\nStrings are escaped by default, but you can pass in `SafeString`s to avoid escaping.\n\n```python\nfrom simple_html.nodes import br, p, SafeString\nfrom simple_html.render import render\n\nnode = p(\n    "Escaped & stuff",\n    br,\n    SafeString("Not escaped & stuff")\n)\n\nrender(node)  # returns: <p>Escaped &amp; stuff<br/>Not escaped & stuff</p> \n```\n\nFor convenience, many tags are provided, but you can create your own as well:\n\n```python\nfrom simple_html.nodes import TagBase \nfrom simple_html.render import render\n\ncustom_elem = TagBase("custom-elem")\n\nrender(\n    custom_elem.attrs(id="some-custom-elem-id")(\n        "Wow"\n    )\n)  # returns: <custom-elem id="some-custom-elem-id">Wow</custom-elem> \n```\n\nLikewise, some attributes have been created as type-safe presets. Note that there are multiple ways to create attributes. \nThe examples below are all equivalent:\n\n```python\nfrom simple_html.attributes import height, id_\nfrom simple_html.nodes import div\n\n\n# **kwargs: recommended for most cases\ndiv.attrs(id="some-id", height="100")\n\n# *args: useful for attributes that may be reserved keywords or when type constraints are desired.\n# Presets, raw tuples, and kwargs can be used interchangeably.\ndiv.attrs(("id", "some-id"), ("height", "100"))\n\ndiv.attrs(("id", "some-id"), height(100))\n\ndiv.attrs(id_("some-id"), height(100))\n\ndiv.attrs(id_("some-id"), height="100")\n\n# each would render to: <div id="some-id" height="100"></div> \n```\n\nYou can build your own presets, using `str_attr`, `int_attr`, or `bool_attr`. For instance, here are\nseveral of the attribute preset definitions\n\n```python\nfrom simple_html.attributes import bool_attr, int_attr, str_attr\n\nchecked = bool_attr(\'checked\')\nclass_ = str_attr(\'class\')\ncols = int_attr(\'cols\')\n```\nBut anything that renders to the type of `Attribute` will work.',
    'author': 'Keith Philpott',
    'author_email': 'fakekeith@example.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/keithasaurus/simple_html',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
