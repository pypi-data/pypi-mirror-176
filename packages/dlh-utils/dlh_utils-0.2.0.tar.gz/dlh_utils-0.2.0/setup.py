# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dlh_utils']

package_data = \
{'': ['*']}

install_requires = \
['graphframes-wrapper>=0.6,<0.7',
 'graphframes>=0.6,<0.7',
 'jellyfish>=0.9,<0.10',
 'pandas>=0.20.1,<0.21.0']

setup_kwargs = {
    'name': 'dlh-utils',
    'version': '0.2.0',
    'description': 'A PySpark package used to expedite and standardise the data linkage process',
    'long_description': '# DLH utils\n\nA package produced by the linkage development team from the Data Linkage Hub, containing a set of functions used to expedite and streamline the data linkage process.\n\nThanks to all those in the Data Linkage Hub and Methodology that have contributed towards this repository.\n\nPlease log an issue on the issue board or contact any of the active contributors with any issues or suggestions for improvements you have.\n\n## Installation steps\n\n* click the \'clone\' button on the project homepage and copy the project\'s HTTP address\n* open a terminal session within CDSW and run `git clone [http_address]`\n* the project files will now be moved to your local file structure, within a folder called "dlh_utils"\n* you can now install the package, typically by running either `!pip3 install \'/home/cdsw/dlh_utils\'` in a workbench/jupyter notebook session, or `pip3 install \'/home/cdsw/dlh_utils\'` in terminal. \n\n**Note: the filepath shown in this example may differ depending on where you have cloned the project.**\n* all finished! You can now import modules from the dlh_utils package like any other Python library\n\n*This package is a work in progress!* We will notify you of significant changes to the package. If you want to upgrade to the latest version, clone the project from GitLab again and run either `!pip3 install -U \'[path_to_dlh_utils]\'` in workbench, or `pip3 install -U \'[path_to_dlh_utils]\'` in terminal, to upgrade your package installation.\n\n## Using the cluster function\n\nThe cluster function uses Graphframes, which requires an extra JAR file dependency to be submitted to your spark context in order for it to run.\n\nAt ONS, we have a graphframes-wrapper package that contains this JAR file. This is included in the package requirements\nas an optional dependency. To install this and use graphframes, run `!pip3 install dlh_utils[full]`\n\nIf outside of ONS you will need to submit graphframes\' JAR file dependency to your spark context. This can be found here:\n\nhttps://repos.spark-packages.org/graphframes/graphframes/0.6.0-spark2.3-s_2.11/graphframes-0.6.0-spark2.3-s_2.11.jar\n\nOnce downloaded, this can be submitted to your spark context via: `spark.conf.set(\'spark.jars\', path_to_jar_file)`',
    'author': 'Anthony Edwards',
    'author_email': 'anthonygedwards93@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Data-Linkage/dlh_utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
