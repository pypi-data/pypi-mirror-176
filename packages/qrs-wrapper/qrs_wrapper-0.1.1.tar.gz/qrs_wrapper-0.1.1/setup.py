# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qrs_wrapper']

package_data = \
{'': ['*']}

install_requires = \
['biosppy>=1.0.0,<2.0.0',
 'neurokit2>=0.2.1,<0.3.0',
 'numpy>=1.23.4,<2.0.0',
 'py-ecg-detectors>=1.3.2,<2.0.0']

setup_kwargs = {
    'name': 'qrs-wrapper',
    'version': '0.1.1',
    'description': '"Produce R peaks estimation on top of libraries specialized in ecg data processing"',
    'long_description': '# QRS-Wrapper\n\n## Overview\nQRS-Wrapper is a python library which:\n- wraps several open source QRS detection python libraries\n- includes a meta algorithm built on top of those open-source algorithms which is supposed to outperform them \n- provides some metrics to assess the quality of those algorithms as well as a nice visualization in a PDF file.\n\n## Installation of QRS-Wrapper\n```bash\npip install qrs-wrapper\n```\n\n## Getting started\nImport qrs-wrapper and load data\n```python\n>>> import qrs_wrapper as qw\n>>> ecg_data, groundtruth_qrs = qw.load_csv(\'path/to/your/csv\')\n```\n\n\nRun existing open source qrs-detection algorithms, for instance:\n```python\n>>> estimated_qrs_1 = qw.qrs_estimation(ecg_data, library="biosppy", method="hamilton")\n>>> estimated_qrs_2 = qw.qrs_estimation(ecg_data, library="neurokit", method="default")\n>>> estimated_qrs_3 = qw.qrs_estimation(ecg_data, library="py-ecg-detectors", method="hamilton")\n```\n\n\nRun meta qrs-detection algorithm\n```python\n>>> estimated_qrs_meta = qw.qrs_meta(ecg_data, (estimated_qrs_1, estimated_qrs_2, estimated_qrs_3))\n```\nUsers can specify the weight of the estimators: qw.qrs_meta(..., weight = usr_weight).\nBy default, it is computed from the prediction they make and how it compares to the other estimators\' prediction.\n\nThe predictions and estimators\' weight help define a likelyhood score for each potential location.\n\nqrs_meta is running a local search and a simutated annealing for which users can also specify the parameters: \nqw.qrs_meta(..., param = usr_param).\n\nThe objective function to optimize is a function of the likelyhood score of the selected locations and of the regularity\nof the solution. The regularity is itself linear combination of the regularity of the R peaks amplitude \nand of the delays between consecutive R peaks. \nThe regularity of the features are measured locally by computung the coefficient of variation cv(X)=std(X)/mean(X) \non small sequences of R peaks all over the solution.\n\nBy default, the parameters of SA and local search are as follows:\nparam = {\n\t"temp_ini" : 830,\t\t\t\t# initial temperature\n      "max_iter" : 5000,\t\t\t# nb. iterations in simulated annealing\n      "cooling_rate" : 0.9989,\t\t# cooling rate at each iteration\n      "sigma" : 800,\t\t\t\t# weight of the location\'s score\n      "rho" : 200,\t\t\t\t# weight of the regularity (gathers amplitude + delay)\n      "alpha" : 1,\t\t\t\t# weight of the amplitude regularity\n      "delta" : 3\t\t\t\t\t# weight of the delay (between consecutive r peaks) regularity\n}\n\nAll parameters are interconnected and had been tuned. \nIt is not recommanded to stray from the default values.\n\n\n\nCompute and plot performance metrics\n```python\n>>> qw.draw_performance(\n    ecg_data,\n    groundtruth_qrs,\n    (estimated_qrs_1, estimated_qrs_2, estimated_qrs_3, estimated_qrs_meta),\n    names = ("biosspy", "neurokit", "py-ecg-detectors", "meta"),\n    output_file="path/to/your/report.pdf"\n)\n```',
    'author': 'GiovanniLB',
    'author_email': 'globianco29@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
