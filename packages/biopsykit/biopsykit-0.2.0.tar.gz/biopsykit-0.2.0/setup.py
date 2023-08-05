# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['biopsykit',
 'biopsykit.carwatch_logs',
 'biopsykit.classification',
 'biopsykit.classification.model_selection',
 'biopsykit.colors',
 'biopsykit.io',
 'biopsykit.metadata',
 'biopsykit.plotting',
 'biopsykit.protocols',
 'biopsykit.questionnaires',
 'biopsykit.saliva',
 'biopsykit.signals',
 'biopsykit.signals.ecg',
 'biopsykit.signals.eeg',
 'biopsykit.signals.imu',
 'biopsykit.signals.imu.feature_extraction',
 'biopsykit.signals.rsp',
 'biopsykit.sleep',
 'biopsykit.sleep.psg',
 'biopsykit.sleep.sleep_endpoints',
 'biopsykit.sleep.sleep_processing_pipeline',
 'biopsykit.sleep.sleep_wake_detection',
 'biopsykit.sleep.sleep_wake_detection.algorithms',
 'biopsykit.stats',
 'biopsykit.utils']

package_data = \
{'': ['*']}

install_requires = \
['IPython>=7.13.0,<8.0.0',
 'XlsxWriter>=1.4.5,<2.0.0',
 'ipympl>=0.7.0,<0.8.0',
 'ipywidgets>=7.6.3,<8.0.0',
 'joblib>=1.0.0,<2.0.0',
 'matplotlib>=3,<4',
 'neurokit2>=0.1.3,<0.2.0',
 'nilspodlib>=3.2.2,<4.0.0',
 'numpy>=1,<2',
 'openpyxl>=3.0.7,<4.0.0',
 'pandas>=1,<2',
 'pingouin>=0.3.12,<0.4.0',
 'scikit-learn>=0.24.2,<0.25.0',
 'scipy>=1.7.1,<2.0.0',
 'seaborn>=0.11.1,<0.12.0',
 'statannot>=0.2.3,<0.3.0',
 'tqdm>=4.62.0,<5.0.0']

extras_require = \
{'mne': ['mne>=0.23.0,<0.24.0']}

setup_kwargs = {
    'name': 'biopsykit',
    'version': '0.2.0',
    'description': 'A python package for the analysis of biopsychological data.',
    'long_description': None,
    'author': 'Robert Richer',
    'author_email': 'robert.richer@fau.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
