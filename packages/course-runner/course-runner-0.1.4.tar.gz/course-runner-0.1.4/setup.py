"""
Setup script for deploying runner on PyPI and allowing to install it using pip.
"""


from setuptools import setup
from typing import List

import runner


def readme() -> str:
    """
    Reads the README file of the project to use it as long description.

    :return: The long description of runner.
    """
    with open('README.md') as file:
        return file.read()


def requirements() -> List[str]:
    """
    Reads the requirements file of the project to use its content to determine
    the dependencies of the package.

    :return: The dependencies of runner.
    """
    return [
        "certifi == 2021.5.30",
        "charset-normalizer == 2.0.3",
        "coverage == 5.5",
        "idna == 3.2",
        "loguru == 0.5.3",
        "nose == 1.3.7",
        "requests == 2.26.0",
        "urllib3 == 1.26.6"
    ]


setup(
    name='course-runner',
    version=runner.__version__,
    packages=[
        'runner'
    ],

    description=runner.__summary__,
    long_description=readme(),
    long_description_content_type='text/markdown',
    keywords=runner.__keywords__,

    author=runner.__author__,
    author_email=runner.__email__,
    url=runner.__uri__,

    install_requires=requirements(),

    test_suite='nose.collector',
    tests_require=['nose'],

    scripts=[
        'bin/course-runner'
    ],

    classifiers=[
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent'
    ],
    license=runner.__license__,

    include_package_data=True,
    zip_safe=False
)
