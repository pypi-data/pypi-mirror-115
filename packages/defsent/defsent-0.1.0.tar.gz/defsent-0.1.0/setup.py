# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['defsent']

package_data = \
{'': ['*']}

install_requires = \
['torch', 'transformers']

setup_kwargs = {
    'name': 'defsent',
    'version': '0.1.0',
    'description': 'DefSent: Sentence Embeddings using Definition Sentences',
    'long_description': '# DefSent: Sentence Embeddings using Definition Sentences\n\n\n## Pretrained checkpoints\n\n| checkpoint | STS12 | STS13 | STS14 | STS15 | STS16 | STS-B | SICK-R | Avg. |\n|--|--|--|--|--|--|--|--|--|\n|defsent-bert-base-uncased-cls|67.61|80.44|70.12|77.5|76.34|75.25|71.71|74.14|\n|defsent-bert-base-uncased-mean|68.24|82.62|72.8|78.44|76.79|77.5|71.69|75.44|\n|defsent-bert-base-uncased-max|65.32|82.00|73.00|77.38|75.84|76.74|71.67|74.57|\n|defsent-bert-large-uncased-cls|67.03|82.41|71.25|80.33|75.43|73.83|73.34|74.8|\n|defsent-bert-large-uncased-mean|63.93|82.43|73.29|80.52|77.84|78.41|73.39|75.69|\n|defsent-bert-large-uncased-max|60.15|80.70|71.67|77.19|75.71|76.90|72.57|73.55|\n|defsent-roberta-base-cls|66.13|80.96|72.59|78.33|78.85|78.51|74.44|75.69|\n|defsent-roberta-base-mean|62.38|78.42|70.79|74.60|77.32|77.38|73.07|73.42|\n|defsent-roberta-base-max|64.61|78.76|70.24|76.07|79.02|78.34|74.54|74.51|\n|defsent-roberta-large-cls|62.47|79.07|69.87|72.62|77.87|79.11|73.95|73.56|\n|defsent-roberta-large-mean|57.8|72.98|69.18|72.84|76.50|79.17|74.36|71.83|\n|defsent-roberta-large-max|64.11|81.42|72.52|75.37|80.23|79.16|73.76|75.22|\n',
    'author': 'hppRC',
    'author_email': 'hpp.ricecake@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://arxiv.org/abs/2105.04339',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
