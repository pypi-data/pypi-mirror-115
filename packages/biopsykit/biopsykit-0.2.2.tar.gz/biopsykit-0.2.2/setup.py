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
 'pandas>=1.2.0,<2.0.0',
 'pingouin>=0.3.12,<0.4.0',
 'scikit-learn>=0.24.2,<0.25.0',
 'scipy>=1.7.1,<2.0.0',
 'seaborn>=0.11.1,<0.12.0',
 'statannot>=0.2.3,<0.3.0',
 'tqdm>=4.62.0,<5.0.0',
 'xlrd>=2.0.1,<3.0.0']

extras_require = \
{'mne': ['mne>=0.23.0,<0.24.0']}

setup_kwargs = {
    'name': 'biopsykit',
    'version': '0.2.2',
    'description': 'A python package for the analysis of biopsychological data.',
    'long_description': '# BioPsyKit\n\n[![PyPI](https://img.shields.io/pypi/v/biopsykit)](https://pypi.org/project/biopsykit/)\n![GitHub](https://img.shields.io/github/license/mad-lab-fau/biopsykit)\n[![Test and Lint](https://github.com/mad-lab-fau/BioPsyKit/actions/workflows/test-and-lint.yml/badge.svg)](https://github.com/mad-lab-fau/BioPsyKit/actions/workflows/test-and-lint.yml)\n![Coverage](./coverage-badge.svg)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/biopsykit)\n![GitHub commit activity](https://img.shields.io/github/commit-activity/m/mad-lab-fau/biopsykit)\n\nA Python package for the analysis of biopsychological data.\n\nWith this package you have everything you need for analyzing biopsychological data, including:\n* Data processing pipelines for biosignals (ECG, EEG, ...)\n* Methods for analyzing saliva samples (cortisol, amylase)\n* Implementation of various psychological and HCI-related questionnaires\n\n \nAdditionally, there are modules to analyze and visualize data acquired from special measurement scenarios, such as:\n* Montreal Imaging Stress Task (MIST)\n* ... more to follow\n\n## Details\n\n### Biosignal Analysis\n#### ECG Processing\n`BioPsyKit` provides a whole ECG data processing pipeline, consisting of:\n* Loading ECG data from:\n    * generic `.csv` files\n    * NilsPod binary (`.bin`) files (requires `NilsPodLib`: https://github.com/mad-lab-fau/NilsPodLib)\n    * from other sensor types (_coming soon_)\n* Splitting data into chunks (based on time intervals) that will be analyzed separately\n* Perform ECG processing, including:\n    * R peak detection (using `Neurokit`: https://github.com/neuropsychology/NeuroKit)\n    * R peak outlier removal and interpolation\n    * HRV feature computation\n    * ECG-derived respiration (EDR) estimation for respiration rate and respiratory sinus arrhythmia (RSA) (_experimental_)\n* Visualization of results\n\n... more biosignals coming soon!\n\n### Biomarker Analysis\n`BioPsyKit` provides several methods for the analysis of biomarkers, such as:\n* Load saliva data (e.g. cortisol and amylase) from deepwell plate Excel exports\n* Compute standard features (maximum increase, slope, AUC, ...)\n\n### Questionnaires\n`BioPsyKit` implements various established psychological and HCI-related questionnaires, such as:\n* Perceived Stress Scale (PSS)\n* Positive Appraisal Negative Appraisal Scale (PANAS)\n* Self-Compassion Scale (SCS)\n* System Usability Scale (SUS)\n* NASA Task Load Index (NASA-TLX)\n* Short Stress State Questionnaire (SSSQ)\n* ...\n\nFor more details, see the instructions in the `questionnaire` module.\n\n### Stress Protocols\n`BioPsyKit` implements methods for analyzing data recorded with several established stress protocols, such as:\n* Montreal Imaging Stress Task (MIST)\n* Trier Social Stress Test (TSST) (_coming soon..._) \n\n\n\n## Installation\nInstall it via pip:\n\n```\npip install biopsykit\n```\n\n\n## For developer\n\n```bash\ngit clone https://github.com/mad-lab-fau/BioPsyKit.git\ncd biopsykit\npoetry install\n```\nInstall Python >3.8 and [poetry](https://python-poetry.org).\nThen run the commands below to get the latest source and install the dependencies:\n\n\nTo run any of the tools required for the development workflow, use the doit commands:\n\n```bash\n$ poetry run doit list\ndocs                 Build the html docs using Sphinx.\nformat               Reformat all files using black.\nformat_check         Check, but not change, formatting using black.\nlint                 Lint all files with Prospector.\ntest                 Run Pytest with coverage.\nupdate_version       Bump the version in pyproject.toml and biopsykit.__init__ .\n```\n\n\n## Examples\nSee Examples in the function documentations on how to use this library.\n',
    'author': 'Robert Richer',
    'author_email': 'robert.richer@fau.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mad-lab-fau/biopsykit',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)
