__copyright__ = "(c) 2016 RenaissanceRe IP Holdings Ltd.  All rights reserved."

import logging
import os
import setuptools
from setuptools import setup, find_packages

LOG = logging.getLogger(__name__)


def parse_requirements(filename, parent):
    def read_file(_filename):
        file_path = os.path.join(parent, _filename)
        with open(file_path) as _file:
            return _file.read()
    content = read_file(filename)
    for line_number, line in enumerate(content.splitlines(), 1):
        candidate = line.strip()
        if candidate.startswith('-r'):
            for item in parse_requirements(candidate[2:].strip(), parent):
                yield item
        else:
            yield candidate


dir_name = os.path.dirname(__file__)
requirements = list(parse_requirements("requirements.txt", dir_name))

LOG.info('Requirements: %s' % requirements)
LOG.info('setup: %s' % __file__)
LOG.info('setuptools: %s' % setuptools.__file__)
LOG.info('setuptools version: %s' % setuptools.__version__)

setup(
    name="prommon",
    use_scm_version=True,
    packages=find_packages(),
    setup_requires=['setuptools_scm'],
    include_package_data=True,
    install_requires=requirements,
)
