# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dfs']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'graph-dfs',
    'version': '0.0.6',
    'description': 'Graphs and Depth First Search',
    'long_description': '# Graph-DFS\n\nThis package allows for the creation of graphs. It also provides the depth first search algorithm.\n\n## Installation\n\n```shell\npip install graph-dfs\n```\n\n## How to use it?\n\nTo create a graph, do:\n\n```python\ng = Graph(n)\n```\n\nwhere `n` is the number of vertices. To create an arc from\nvertex `a` to vertex `b`, do:\n\n```python\ng.link(a, b)\n```\n\nwhere `a` and `b` are indices in the range `[0, n - 1]`. You can perform a depth first search on the graph\nwith:\n\n```python\ndfs = DFS(g)\ndfs.start()\n```\n\nIf you desire to obtain a topological sorting of the graph, then do so after a DFS with:\n\n```python\ndfs.opological_sorting()\n```\n',
    'author': 'Daniel M. Martin',
    'author_email': 'danielmmartin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/daniel-ufabc/graph-dfs',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
