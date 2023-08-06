# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['imputr', 'imputr.domain', 'imputr.imputers', 'imputr.strategy']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.3,<2.0', 'scikit-learn>=1.0.2,<2.0.0']

setup_kwargs = {
    'name': 'imputr',
    'version': '0.1.0',
    'description': 'Imputing missing values in your data science.',
    'long_description': '\n<p align="center">\n  <img src="https://github.com/imputr/imputr/blob/release-v.0.1/docs/docs/_static/imputr-logo-horizontal.svg?raw=true" width="800">\n</p>\n\n\n# ****🎯\xa0What is Imputr?****\n\nImputr is an open-source library that allows users to stably impute tabular data sets with ML-based and conventional techniques. It is designed to have an extremely simple, yet extensive API, making it possible for users of all levels and tasks to deploy the library in their workflows. \n\n\n<p align="center">\n <img src="https://github.com/imputr/imputr/blob/release-v.0.1/docs/docs/_static/imputation.gif?raw=true" width="600">\n</p> \n \n# 🚀\xa0Getting started\n\n**Install Imputr with PIP:**\n\n```bash\npip install imputr\n```\n\n## AutoImputer\n\nHere is an example of the simplest usage of the AutoImputer (our recommended workflow for newbies and intermediates), which by default automatically imputes the missing values for all columns with a modern version of the [missForest](https://arxiv.org/pdf/1105.0828.pdf) algorithm.\n\n```python\nfrom imputr.autoimputer import AutoImputer\nimport pandas as pd\n\n# Import dataset into Pandas DataFrame\ndf = pd.read_csv("example.csv")\n\n# Initialize AutoImputer with data - set exec_now=False to delay imputation \nimputer = AutoImputer(data=df)\n\n# Retrieve imputed dataset from AutoImputer object\nimputed_df = imputer.get_result()\n```\n\nHere you can see an example of how the AutoImputer works internally.\n\n<p align="center">\n <img src="https://github.com/imputr/imputr/blob/release-v.0.1/docs/docs/_static/autoimputer.gif?raw=true" width="600" align="center">\n</p>\n\nTo see what else be done with the AutoImputer API to customise its behaviour, reference our [documentation](https://imputr.readthedocs.io/en/latest/examples.html).\n\n\n\n# 📕\xa0Documentation\n\nMultiple links to documentation:\n\n- [Imputr API](https://imputr.readthedocs.io/en/latest/autoapi/index.html)\n- [Imputr concepts](https://imputr.readthedocs.io/en/latest/concepts.html)\n- [Core class structure](https://imputr.readthedocs.io/en/latest/coreclass.html)\n- [Medium blogs for more information](https://medium.com/tag/imputr)\n- [Our Slack channel](https://join.slack.com/t/imputr/shared_invite/zt-1jnbwuv0l-T5xd0Akr3ab5jr2RprF_ZA)\n- [More real world examples](https://imputr.readthedocs.io/en/latest/examples.html)\n\n# 👨🏽\u200d💻\xa0Contribution\n\nImputr is an ever-evolving open source library and can always use contributors who want to help build with the community.\n\nSee the [Contribution Jumpstart](https://imputr.readthedocs.io/en/latest/contributionjumpstart.html) page to get started with your first contribution!\n\n---\n\nImputr is distributed under an Apache License Version 2.0. A complete version can be found\xa0[here](https://github.com/imputr/imputr/blob/main/LICENSE). All future contributions will continue to be distributed under this license.',
    'author': 'Rauf Akdemir',
    'author_email': 'orhanrauf@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
