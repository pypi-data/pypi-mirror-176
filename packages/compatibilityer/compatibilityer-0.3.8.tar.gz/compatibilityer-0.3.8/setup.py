# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['compatibilityer']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'compatibilityer',
    'version': '0.3.8',
    'description': 'Tool to convert Python code to work with older versions',
    'long_description': 'Python3.11などの新しいバージョンのコードを、古いバージョンで動作するように変換するツールです。\n\nあくまでも動作するように小手先の変換を施すだけであって、複雑なパターンの変換や厳密な等価性が必要な場合には使用できません。\nまた、当然ですが可読性はある程度失われます。\n\n具体的には、以下のような変換を行います。\n- 代入や関数定義の型アノテーションを文字列リテラルに置き換える\n- 旧バージョンに存在しない要素の `from typing import` を削除する\n- `alias: TypeAlias = SomeType` という形の `TypeAlias` の定義をする代入文の右辺を文字列リテラルに置き換える\n- match文をif文に変換する(複雑なものには未対応)\n',
    'author': 'nahco314',
    'author_email': 'nahco3_ta@yahoo.co.jp',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
