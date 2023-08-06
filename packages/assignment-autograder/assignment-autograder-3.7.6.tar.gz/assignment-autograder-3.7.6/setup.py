# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autograder',
 'autograder.plagiarism_detection',
 'autograder.plagiarism_detection.lexers',
 'autograder.testcase_types.cpython',
 'autograder.testcase_types.cpython.helpers',
 'autograder.testcase_types.cpython.templates',
 'autograder.testcase_types.cpython.templates.tests.testcases',
 'autograder.testcase_types.gcc',
 'autograder.testcase_types.javac',
 'autograder.testcase_utils']

package_data = \
{'': ['*'],
 'autograder.testcase_types.cpython.templates': ['tests/output/*'],
 'autograder.testcase_types.gcc': ['c++_templates/*',
                                   'c++_templates/tests/output/*',
                                   'c++_templates/tests/testcases/*',
                                   'c_templates/*',
                                   'c_templates/tests/output/*',
                                   'c_templates/tests/testcases/*',
                                   'helpers/*',
                                   'memleak/*'],
 'autograder.testcase_types.javac': ['extra/*',
                                     'helpers/*',
                                     'templates/*',
                                     'templates/tests/output/*',
                                     'templates/tests/testcases/*']}

install_requires = \
['antlr4-python3-runtime==4.9.2',
 'numba>=0.56.2,<0.57.0',
 'numpy>=1.22.4,<2.0.0',
 'tomlkit>=0.11.4,<0.12.0']

entry_points = \
{'console_scripts': ['autograder = autograder.__main__:main']}

setup_kwargs = {
    'name': 'assignment-autograder',
    'version': '3.7.6',
    'description': 'A simple, secure, and versatile way to automatically grade programming assignments',
    'long_description': '## Warning\n\nThis package is deprecated. Please, use [autograder](https://pypi.org/project/autograder/) package instead.\n',
    'author': 'Ovsyanka',
    'author_email': 'szmiev2000@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Ovsyanka83/autograder',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
