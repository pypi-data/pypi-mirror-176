# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['boots']

package_data = \
{'': ['*']}

install_requires = \
['joblib>=1.2.0,<2.0.0', 'numpy>=1.23.4,<2.0.0', 'vose>=0.0.1,<0.0.2']

setup_kwargs = {
    'name': 'boots',
    'version': '0.1.2',
    'description': 'A tiny statistical bootstraping library.',
    'long_description': "# 🥾 Boots 👢 - A Tiny Bootstrapping Library\n\nThis is a tiny library for doing bootstrap sampling and estimating. It pulls together various tricks to make the process as fast and painless as possible. The tricks included are:\n\n- Parallel execution with [`joblib`](https://joblib.readthedocs.io/en/latest/parallel.html) \n- [The Bayesian bootstrap](https://matteocourthoud.github.io/post/bayes_boot/) with two-level sampling.\n- The [Vose method](https://github.com/MaxHalford/vose) for fast weighted sampling with replacement\n\n**Install**\n\n```bash\npip install boots\n```\n\nFor development:\n\n```bash\npip install git+https://github.com/pmbaumgartner/boots\n```\n\n## Example\n\n```python\nfrom boots import bootstrap\nimport numpy as np\n\nx = np.random.pareto(2, 100)\n\nsamples = bootstrap(\n    data=x,\n    statistic=np.median,\n    n_iterations=1000,\n    seed=1234,\n    n_jobs=-1\n)\n\n# bayesian two-level w/ 4 parallel jobs\nsamples = bootstrap(\n    data=x,\n    statistic=np.median, \n    n_iterations=1000, \n    seed=1234, \n    n_jobs=4, \n    bayesian=True\n)\n\n# do something with it\nimport pandas as pd\nposterior = pd.Series(samples)\nposterior.describe(percentiles=[0.025, 0.5, 0.975])\n```\n\n**Paired Statistics**\n\n```python\nfrom boots import bootstrap\nimport numpy as np\n\n\n# generate some fake correlated data by sorting two arrays and adding some noise\na = np.sort(np.random.normal(0, 1, 100)) + np.random.normal(0, 1, 100)\nb = np.sort(np.random.normal(0, 1, 100)) + np.random.normal(0, 1, 100)\npairs = list(zip(a, b))\n\n# for paired (or row-wise) metrics you might need to\n# create a wrapper function that unpacks\n# each row's values into array arguments for your metric function\ndef corr_unwrap(pairs):\n    a1, a2 = zip(*pairs)\n    corr = np.corrcoef(a1, a2)[0, 1]\n    return corr\n\n\nsamples = bootstrap(\n    data=pairs,\n    statistic=corr_unwrap,\n    n_iterations=1000,\n    seed=1234,\n    n_jobs=-1,\n    bayesian=True\n)\n\nimport pandas as pd\nposterior = pd.Series(samples)\nposterior.describe(percentiles=[0.025, 0.5, 0.975])\n```\n\n",
    'author': 'Peter Baumgartner',
    'author_email': '5107405+pmbaumgartner@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
