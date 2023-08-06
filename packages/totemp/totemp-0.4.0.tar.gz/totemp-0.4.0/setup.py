# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['totemp']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'totemp',
    'version': '0.4.0',
    'description': 'Temperature Converter',
    'long_description': '# ToTemp\n<div style="display: inline-block">\n  <img src="https://shields.io/pypi/v/totemp"  alt="package version"/>\n  <img src="https://img.shields.io/pypi/l/totemp.svg"  alt="license"/>\n</div>\n\n**ToTemp** is a temperature conversion package between Celsius, Delisle, Fahrenheit, Kelvin, Rankine, Reaumur, Newton and Romer\n\n## Usage\n\nFirst of all, install the package:\n\n```\npip install totemp\n```\n\nor, to have an example in poetry environments:\n\n```\npoetry add --group dev totemp\n```\n\nThen, just use it:\n\n> In these examples, you can observe the methods working with all\navailable Classes in this package\n\n````python\n# Import Celsius class\nfrom totemp import Celsius\n\ntemperature = Celsius.to_fahrenheit(35)\nprint(temperature)  # 95.0 -> float\n\ntemperature = Celsius.to_fahrenheit(35, float_ret=False)\nprint(temperature)  # 95 -> int\n````\n````python\n# Import Fahrenheit class\nfrom totemp import Fahrenheit\n\ntemperature = Fahrenheit.to_newton(18.746)\nprint(temperature)  # -2.4299000000000004 -> float\n\ntemperature = Fahrenheit.to_newton(18.746, float_ret=False)\nprint(temperature)  # -2 -> int\n````\n````python\n# Import Delisle class\nfrom totemp import Delisle\n\ntemperature = Delisle.to_romer(37263.271)\nprint(temperature)  # -12982.14485 -> float\n\ntemperature = Delisle.to_romer(37263.271, float_ret=False)\nprint(temperature)  # -12982 -> int\n````\n````python\n# Import Kelvin class\nfrom totemp import Kelvin\n\ntemperature = Kelvin.to_reaumur(44.28137746)\nprint(temperature)  # -183.094898032 -> float\n\ntemperature = Kelvin.to_reaumur(44.28137746, float_ret=False)\nprint(temperature)  # -183 -> int\n````\n````python\n# Import all classes\nimport totemp as tp\n\ntemperature = tp.Celsius.to_delisle(345.797)\nprint(temperature)  # -368.69550000000004 -> float\n\ntemperature = tp.Celsius.to_delisle(345.797, float_ret=False)\nprint(temperature)  # -368 -> int\n\ntemperature = tp.Fahrenheit.to_rankine(500)\nprint(temperature)  # 959.6700000000001 -> float\n\ntemperature = tp.Fahrenheit.to_rankine(500, float_ret=False)\nprint(temperature)  # 959 -> int\n\ntemperature = tp.Delisle.to_kelvin(12.5887)\nprint(temperature)  # 364.7575333333333 -> float\n\ntemperature = tp.Delisle.to_kelvin(12.5887, float_ret=False)\nprint(temperature)  # 364 -> int\n\ntemperature = tp.Kelvin.to_romer(44.28137746)\nprint(temperature)  # -112.6560268335 -> float\n\ntemperature = tp.Kelvin.to_reaumur(44.28137746, float_ret=False)\nprint(temperature)  # -112 -> int\n````\n\nNote that **all returns are *float values*** if you don\'t specify "float_ret"\nparameter as False, which is True by default and that **applies to all methods**.\n\nAll methods have two parameters, the **value** (which is positional-only)\nand the **return type** (which is <float_ret>, that is by default True to return float\nvalues and keyword-only)\n\n## Package Versions\n\n---\n\n- _0.1.0_:\n  - Yanked, not functional;\n- _0.2.0_:\n  - Functional;\n  - Can convert Celsius to Delisle, Fahrenheit, Kelvin, Newton, Rankine, Réaumur and Rømer.\n- _0.3.0_:\n  - Changed methods implementations and adds Fahrenheit conversions;\n      - <scale_value> parameter is now positional-only;\n      - Adds new parameter -> float_ret -> Float Return (True by default, keyword-only);\n      - Celsius class methods were updated and enhanced;\n      - Can now convert Fahrenheit to Celsius, Delisle, Kelvin, Newton, Rankine, Réaumur and Rømer.\n\n\n- **0.4.0**:\n  - There are **two new Classes**, **Kelvin** and **Delisle**, functional and ready-to-use.\n---\n\n## License\n\nFor more information, check LICENSE file.\n',
    'author': 'Edson Pimenta',
    'author_email': 'edson.tibo@gmail.com',
    'maintainer': 'Edson Pimenta',
    'maintainer_email': 'edson.tibo@gmail.com',
    'url': 'https://github.com/eddyyxxyy/ToTemp',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
