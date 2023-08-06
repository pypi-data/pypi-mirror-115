# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kiez',
 'kiez.analysis',
 'kiez.evaluate',
 'kiez.hubness_reduction',
 'kiez.io',
 'kiez.neighbors',
 'kiez.neighbors.approximate',
 'kiez.neighbors.exact',
 'kiez.utils']

package_data = \
{'': ['*']}

install_requires = \
['annoy>=1.17.0,<2.0.0',
 'class-resolver>=0.0.13,<0.0.14',
 'importlib-metadata',
 'joblib>=1.0.0,<2.0.0',
 'ngt>=1.12.2,<2.0.0',
 'nmslib>=2.1.1,<3.0.0',
 'numpy>=1.20.0,<2.0.0',
 'pandas>=1.2.1,<2.0.0',
 'scikit-learn>=0.24.1,<0.25.0',
 'scipy>=1.6.0,<2.0.0',
 'tqdm>=4.56.0,<5.0.0']

extras_require = \
{'docs': ['sphinx>=4.0.2,<5.0.0', 'insegel>=1.1.0,<2.0.0']}

setup_kwargs = {
    'name': 'kiez',
    'version': '0.3.0',
    'description': 'Hubness reduced nearest neighbor search for entity alignment with knowledge graph embeddings',
    'long_description': '<p align="center">\n<img src="https://github.com/dobraczka/kiez/raw/main/docs/kiezlogo.png" alt="kiez logo", width=200/>\n</p>\n\n<h2 align="center"> kiez</h2>\n\n<p align="center">\n<a href="https://github.com/dobraczka/kiez/actions/workflows/main.yml"><img alt="Actions Status" src="https://github.com/dobraczka/kiez/actions/workflows/main.yml/badge.svg?branch=main"></a>\n<a><img alt="Test coverage" src="https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/dobraczka/7c57dda3b055c972a06f0f076df46196/raw/test.json"></a>\n<a href="https://github.com/dobraczka/kiez/blob/main/LICENSE"><img alt="License BSD3 - Clause" src="https://img.shields.io/badge/license-BSD--3--Clause-blue"></a>\n<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n</p>\n\nA Python library for hubness reduced nearest neighbor search for the task of entity alignment with knowledge graph embeddings. The term kiez is a [german word](https://en.wikipedia.org/wiki/Kiez) that refers to a city neighborhood.\n\n## Hubness Reduction\nHubness is a phenomenon that arises in high-dimensional data and describes the fact that a couple of entities are nearest neighbors (NN) of many other entities, while a lot of entities are NN to no one.\nFor entity alignment with knowledge graph embeddings we rely on NN search. Hubness therefore is detrimental to our matching results.\nThis library is intended to make hubness reduction techniques available to data integration projects that rely on (knowledge graph) embeddings in their alignment process. Furthermore kiez incorporates several approximate nearest neighbor (ANN) libraries, to pair the speed advantage of approximate neighbor search with increased accuracy of hubness reduction.\n\n## Installation\nYou can install kiez via pip:\n``` bash\npip install kiez\n```\n\n## Usage\nSimple nearest neighbor search for source entities in target space:\n``` python\nfrom kiez import Kiez\nimport numpy as np\n# create example data\nrng = np.random.RandomState(0)\nsource = rng.rand(100,50)\ntarget = rng.rand(100,50)\n# fit and get neighbors\nk_inst = Kiez()\nk_inst.fit(source, target)\nnn_dist, nn_ind = k_inst.kneighbors()\n```\nUsing ANN libraries and hubness reduction methods:\n``` python\nfrom kiez import Kiez\nimport numpy as np\n# create example data\nrng = np.random.RandomState(0)\nsource = rng.rand(100,50)\ntarget = rng.rand(100,50)\n# prepare algorithm and hubness reduction\nfrom kiez.neighbors import HNSW\nhnsw = HNSW(n_candidates=10)\nfrom kiez.hubness_reduction import CSLS\nhr = CSLS()\n# fit and get neighbors\nk_inst = Kiez(n_neighbors=5, algorithm=hnsw, hubness=hr)\nk_inst.fit(source, target)\nnn_dist, nn_ind = k_inst.kneighbors()\n```\n\n## Documentation\nYou can find more documentation on [readthedocs](https://kiez.readthedocs.io)\n\n## Benchmark\nThe results and configurations of our experiments can be found in a seperate [benchmarking repository](https://github.com/dobraczka/kiez-benchmarking)\n\n## License\n`kiez` is licensed under the terms of the BSD-3-Clause [license](LICENSE.txt).\nSeveral files were modified from [`scikit-hubness`](https://github.com/VarIr/scikit-hubness),\ndistributed under the same [license](external/SCIKIT_HUBNESS_LICENSE.txt).\nThe respective files contain the following tag instead of the full license text.\n\n        SPDX-License-Identifier: BSD-3-Clause\n\nThis enables machine processing of license information based on the SPDX\nLicense Identifiers that are here available: https://spdx.org/licenses/\n',
    'author': 'Daniel Obraczka',
    'author_email': 'obraczka@informatik.uni-leipzig.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dobraczka/kiez',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
