# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['trattoria']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.16', 'scipy>=1.5', 'trattoria-core==0.4.3']

setup_kwargs = {
    'name': 'trattoria',
    'version': '0.3.4',
    'description': 'The fastest streaming algorithms for your TTTR data',
    'long_description': '# 🍕 Trattoria 🍕\nTrattoria delivers you the fastest streaming algorithms to analyze your TTTR data. We\ncurrenlty support the following algorithms:\n- __Second order autocorrelations__: Calculate the autocorrelation between two channels of\n  your TCSPC.\n- __Third Order autocorrelations__: Calculate the coincidences between 3 channels. A sync\nversion is provided were it uses the fact that the sync channel is periodic and known.\n- __Intensity time trace__: Calculate the intensity on each (or all) channels versus time.\n- __Zero finder__: Given two uncorrelated channels (e.g. a laser behind a 50/50 splitter)\n  compute the delay between the input channels.\n- __Lifetime__: Compute the lifetime histogram from a pulsed excitation experiment.\n\n## Supported file formats\nCurrently Trattoria can only read PTU files from PicoQuant. If you want support\nfor more or want to help providing it please put a ticket on the tttr-toolbox\nproject.\n\n## Installing\n```\npip install trattoria\n```\n\n## Examples\nThe entry point to Trattoria is the PTUFile class. This class has methods that\ngive us access to the algorithms. Each of the algorithms takes as input a\nparameter object and returns a results object. For a complete list of the\nfunctionality see the `examples` folder.\n\n```python\nimport trattoria\n\nimport matplotlib.pyplot as plt\n\nptu_filepath = Path("/path/to/some.ptu")\nptu = trattoria.PTUFile(ptu_filepath)\n\ntimetrace_params = trattoria.TimeTraceParameters(\n    resolution=10.0,\n    channel=None,\n)\ntt_res = ptu.timetrace(timetrace_params)\n\nplt.plot(tt_res.t, tt_res.tt / timetrace_params.resolution)\nplt.xlabel("Time (s)")\nplt.ylabel("Intensity (Hz)")\nplt.show()\n```\n\nThe examples folders contains examples of all the functionality available in\nTrattoria.  For more details check the docstrings in `core.py`.\n\n## Design\nTrattoria is just a very thin wrapper around the\n[trattoria-core](https://github.com/GCBallesteros/trattoria-core) library which\nitselfs provides a lower level interface to the the\n[tttr-toolbox](https://github.com/GCBallesteros/tttr-toolbox/tree/master/tttr-toolbox)\nlibrary. A Rust project that provides the compiled components that allows us to\ngo fast.\n\n## Changelog\n### 0.3.4\n- The g2 algorithm now supports a mode flag. With "symmetric" we use the\n  prefered version of the algorithm that returns negative and positive delays.\n  "asymmetric" returns only positive delays but is faster. Default is\n  "symmetric".\n\n### 0.3.3\n- The underlying TTTR Toolbox and Trattoria Core were refactored to support\n  multiple custom ranges or records at once. `start_range` and `stop_range`\n  have disappeared in favor of `record_ranges`. It takes a list of tuples of\n  integers or `None`.\n\n## Citing\n\n',
    'author': 'Guillem Ballesteros',
    'author_email': 'dev+pypi@maxwellrules.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/GCBallesteros/trattoria',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
