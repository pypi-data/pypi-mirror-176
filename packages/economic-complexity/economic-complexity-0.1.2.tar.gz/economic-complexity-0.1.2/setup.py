# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['economic_complexity']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.18.0,<2.0.0', 'pandas>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'economic-complexity',
    'version': '0.1.2',
    'description': 'Functions to calculate Economic Complexity indicators.',
    'long_description': 'This package contains functions to calculate Economic Complexity indicators.  \nThe functions handle the data through `pandas.DataFrame` objects.\n\n<p>\n<a href="https://github.com/Datawheel/py-economic-complexity"><img src="https://flat.badgen.net/github/release/Datawheel/py-economic-complexity" /></a>\n<a href="https://github.com/Datawheel/py-economic-complexity/blob/master/LICENSE"><img src="https://flat.badgen.net/github/license/Datawheel/py-economic-complexity" /></a>\n<a href="https://github.com/Datawheel/py-economic-complexity/"><img src="https://flat.badgen.net/github/checks/Datawheel/py-economic-complexity" /></a>\n<a href="https://github.com/Datawheel/py-economic-complexity/issues"><img src="https://flat.badgen.net/github/issues/Datawheel/py-economic-complexity" /></a>\n</p>\n\n## Installation\n\nWe recommend the use of `poetry`, to resolve the best version of the dependencies that works with your current project.\n\n```bash\n$ poetry add economic-complexity\n```\n\n## Tutorial\n\nWe have [a brief Tutorial](https://github.com/Datawheel/py-economic-complexity/blob/main/docs/TUTORIAL.ipynb), using data from the Observatory of Economic Complexity, to get started on how to use the basic functions of this package.  \nMore complex functions use the resulting dataframes of the basic functions as arguments.\n\n## References\n\n* Hidalgo, César A. (2021). Economic complexity theory and applications. _Nature Reviews Physics, 3_(2), 92–113. https://doi.org/10.1038/s42254-020-00275-1\n\n* Catalán, P., Navarrete, C., & Figueroa, F. (2020). The scientific and technological cross-space: Is technological diversification driven by scientific endogenous capacity? _Research Policy, 104016_, 104016. https://doi.org/10.1016/j.respol.2020.104016\n\n* Hidalgo, César A., & Hausmann, R. (2009). The building blocks of economic complexity. _Proceedings of the National Academy of Sciences of the United States of America, 106_(26), 10570–10575. https://doi.org/10.1073/pnas.0900943106\n\n* Hidalgo, C. A., Klinger, B., Barabási, A.-L., & Hausmann, R. (2007). The product space conditions the development of nations. _Science (New York, N.Y.), 317_(5837), 482–487. https://doi.org/10.1126/science.1144581\n\n* Hartmann, D., Guevara, M. R., Jara-Figueroa, C., Aristarán, M., & Hidalgo, C. A. (2017). Linking Economic Complexity, Institutions, and Income Inequality. _World Development_, 93, 75–93. https://doi.org/10.1016/j.worlddev.2016.12.020\n\n* Romero, J. P., & Gramkow, C. (2021). Economic complexity and greenhouse gas emissions. _World Development_, 139, 105317. https://doi.org/10.1016/j.worlddev.2020.105317\n\n* Bahar, D., Hausmann, R., Hidalgo, C. A. (2014). Neighbors and the evolution of the comparative advantage of nations: Evidence of international knowledge diffusion?. _Journal of International Economics_, 92, 111-123. http://dx.doi.org/10.1016/j.jinteco.2013.11.001\n\n---\n&copy; 2022 [Datawheel, LLC.](https://www.datawheel.us/)  \nThis project is licensed under [MIT](./LICENSE).\n',
    'author': 'Jelmy Hermosilla',
    'author_email': 'jelmy@datawheel.us',
    'maintainer': 'Francisco Abarzua',
    'maintainer_email': 'francisco@datawheel.us',
    'url': 'https://github.com/Datawheel/py-economic-complexity',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
