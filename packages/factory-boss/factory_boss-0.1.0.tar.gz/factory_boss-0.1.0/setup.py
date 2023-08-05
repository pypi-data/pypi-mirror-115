# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['factory_boss', 'factory_boss.scripts', 'factory_boss.spec_parser']

package_data = \
{'': ['*']}

install_requires = \
['Faker>=8.1.4,<9.0.0', 'PyYAML>=5.4.1,<6.0.0', 'lark>=0.11.3,<0.12.0']

extras_require = \
{':python_version < "3.9"': ['graphlib_backport>=1.0.0,<2.0.0']}

setup_kwargs = {
    'name': 'factory-boss',
    'version': '0.1.0',
    'description': 'Fake entire data schemas.',
    'long_description': '# Factory Boss\n\nFake entire data schemas. Easily.\n\nOriginal repository:\n[https://github.com/mariushelf/factory_boss](https://github.com/mariushelf/factory_boss)\n\n# Use case\n\nFactory Boss can help you whenever you need to mock data schemas, for example when\nyou cannot work or develop with the original data for privacy, GDPR related issues\nand security concerns.\n\n# Features\n\nFactory Boss can mock entire data schemas, including relationships and dependencies\nbetween features and objects.\n\nSchema specifications are read from a simple yaml format.\nThe generated output is a list of dictionaries for each mocked entity, which can\neasily be written to a database, converted to pandas DataFrames etc.\n\n\n# Installation\n\nThis package is available on PyPI and can be installed with `pip install factory_boss`.\n\n\n# Usage\n\nMocking a data schema consists of two steps:\n\n1. Specify the schema.\n2. Generate data.\n\n\n## Specify a schema\n\nSchemas are specified in yaml, including relationships between entities and mock\nrules.\n\nSee [simple_schema.yaml](examples/simple_schema.yaml) for an example.\n\n\n## Generate mock data\n\n\n```python\nfrom pprint import pprint\nimport yaml\nfrom factory_boss.generator import Generator\nfrom factory_boss.spec_parser.parser import SpecParser\n\nwith open("examples/simple_schema.yaml", "r") as f:\n    schema = yaml.safe_load(f)\n\nparser = SpecParser()\nparsed_spec = parser.parse(schema)\n\ngenerator = Generator(parsed_spec)\ninstances = generator.generate()\nprint("INSTANCES")\nprint("=========")\npprint(instances)\n```\n\nSee [factory_boss/scripts/generate.py](factory_boss/scripts/generate.py) for\nthe full script.\n\n\n# Roadmap\n\nMany much, above all documentation.\n\nHere are biggest "milestones":\n\n1. documentation\n2. finalize the schema specification\n3. support dynamic fields (generate fields via a Python function with other\n   fields as input)\n\nIn the [issues section](https://github.com/mariushelf/factory_boss/issues)\nthere are some more tickets.\n\n\n# Contributing\n\nI\'m more than happy to accept help in the form of bug reports, feature requests,\nor pull requests, even though there is no formal "contribution guideline" yet.\n\nIf you want to help just reach out to me :)\n\n\n# Acknowledgements\n\nThis work wouldn\'t be possible without the amazing\n[faker](https://github.com/joke2k/faker) package.\n\nFactory Boss is also heavily inspired by\n[factory_boy](https://github.com/FactoryBoy/factory_boy),\nbut has a different focus. While factory_boy excels at generating single objects\nand test fixtures, Factory Boss aims at faking entire data schemas. In that sense\nit offers both a subset and a superset of factory_boy\'s features.\n\n\n# License\n\nMIT -- see [LICENSE](LICENSE)\n\nAuthor: Marius Helf ([helfsmarius@gmail.com](mailto:helfsmarius@gmail.com))\n',
    'author': 'Marius Helf',
    'author_email': 'helfsmarius@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mariushelf/factory_boss',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
