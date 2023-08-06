# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kinetix']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.1.3', 'networkx>=2.5', 'pandas>=1.1.5', 'seaborn>=0.12.0']

entry_points = \
{'console_scripts': ['kinetix = kinetix.runner:main']}

setup_kwargs = {
    'name': 'kinetix',
    'version': '0.1.0',
    'description': 'A simple lightweight library for simulating and plotting enzyme kinetics',
    'long_description': '# Kinetix - A simple enzyme kinetics simulation framework\n\nThis is a simple framework for single / multiple reaction enzyme kinetics simulation and plotting.\nIt allows one to plot reaction kinetics that follows the reversible [Michaelis - Menten](https://en.wikipedia.org/wiki/Michaelis%E2%80%93Menten_kinetics) model.\n\n## Usage\nOne can use the library to produce figures via a command line interface or programmatically (see below for examples)\n\n### CLI\n#### Single reaction\n\nAs an example, the reaction kinetics of Glucose Kinase (EC: [2.7.1.2](https://www.brenda-enzymes.org/enzyme.php?ecno=2.7.1.2) is displayed as an example)\n<p align="center">\n  <img src="https://upload.wikimedia.org/wikipedia/commons/8/8d/Glucokinase.png" />\n</p>\nFirst, create a definition file in YAML format, that defines the reaction parameters:\n\n```yaml\nname: "Glucose kinase simulation"\nreactants: #Concentration of the reactants at the beginning of the reaction (mM)\n  glucose: 0.2\n  glucose_6_p: 0.0\nenzymes: #Concentration of the enzyme(s) at the begining of the reaction (mM)\n  gluk: 0.05 \nreaction: #Kinetic parameters of each of the enzymes for the forward and backward steps of the (reversible) reaction. Note that non-reversible reactions can simple be modeled with high Km for on of the directions.\n  gluk: \n    fwd: "glucose"\n    back: "glucose_6_p"\n    km_fwd: 0.24\n    km_back: 21\n    kcat_fwd: 61\n    kcat_back: 15.9\n```\n\nThen, run the simulation with a simple command line and a few arguments:\n```\npython ./code/runner.py examples/glucose_kinase.yaml --plot_out gluc.png --csv_out gluc.csv\n```\nA figure showing the progression of the reaction as a function of time is generated:\n<p align="center">\n  <img src="examples/figures/gluc.svg" />\n</p>\n\nA csv file containing the data used to generate the figure can also optionally be generated and saved (using the `--csv_out` flag)\n\n#### A pathway\nKinetix can also simulate a pathway composed of several enzymes. This example shows a pathway composed of 3 different enzymes used in the production of [allulose](https://en.wikipedia.org/wiki/Psicose) (D-psicose) a C3 epimer of fructose:\n\n1. **Fructose kinase** (for the production of fructose-6-phosphate)\n2. **D-psicose-3-epimerase** (converting fructose-6-phosphate to allulose-6-phosphate)\n3. **Alkaline phosphatase** (converting allulose-6-phosphate to allulose)\n\n\nThe flow is similar to the one-enzyme case. First, define a yaml file with all the parameters:\n\n```yaml\n---\nname: "Allulose synthesis from fructose"\nreactants:\n  fructose: 1.8\n  fructose_6_p: 0.0\n  allulose: 0.0\n  allulose_6_p: 0.0\nenzymes:\n  fruk: 0.05\n  alsE: 0.05\n  phosphatase: 0.05\nreaction:\n  fruk:\n    fwd: "fructose_6_p"\n    back: "fructose"\n    km_fwd: 0.24\n    km_back: 21\n    kcat_fwd: 61\n    kcat_back: 15.9\n  alsE:\n    fwd: "allulose_6_p"\n    back: "fructose_6_p"\n    km_fwd: 1.6 \n    km_back: 1.6 \n    kcat_fwd: 46\n    kcat_back: 46\n  phosphatase:\n    fwd: "allulose"\n    back: "allulose_6_p"\n    km_fwd: 1 \n    km_back: 100\n    kcat_fwd: 100\n    kcat_back: 1\n```\n\nThen, invoke the application just as before:\n```\n./code/runner.py examples/allulose.yaml --plot_out examples/figures/alu.svg --csv_out examples/csvs/alu.csv\n```\n\nTo produce the reaction figure, which displays the concentration of each of the reactants as a function of time:\n<p align="center">\n  <img src="examples/figures/alu.svg" />\n</p>\n\n### Programmatic Access\nKinetix also makes it really easy to simulate and plot a reaction more flexibly via a simple API.\nExample:\n\nhttps://github.com/LiorZ/Kinetix/blob/4d1107d3e85c45d8d3f222428936ef82c658f223/examples/programmatic.py#L8-L44\n',
    'author': 'Lior Zimmerman',
    'author_email': 'zimmerman.lior@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
}


setup(**setup_kwargs)
