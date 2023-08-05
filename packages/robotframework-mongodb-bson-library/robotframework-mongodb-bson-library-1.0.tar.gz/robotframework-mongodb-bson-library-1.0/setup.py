#!/usr/bin/env python


"""Setup script for Robot's MongoDB Library distributions"""

import setuptools

import sys, os

sys.path.insert(0, os.path.join('src', 'MongoDBBSONLibrary'))

requirements = [
    'tox>=3.0.0',
    'coverage',
    'robotframework>=3.0',
    'pymongo>=3.8.0',
    'bson>=0.5.8'
]

test_requirements = [
    # TODO: put package test requirements here
]

CLASSIFIERS = """
Development Status :: 5 - Production/Stable
License :: Public Domain
Operating System :: OS Independent
Programming Language :: Python
Topic :: Software Development :: Testing
"""[1:-1]


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


from version import VERSION

def main():
    setuptools.setup(name='robotframework-mongodb-bson-library',
                     version=VERSION,
                     description='Mongo Database utility library for Robot Framework that uses bson serialization utils',
                     long_description=long_description,
                     long_description_content_type="text/markdown",
                     author='momen heragi',
                     author_email='momenh@gmail.com',
                     url='https://github.com/momenh/robotframework-mongodb-bson-library',
                     keywords=['mongodb', 'robotframework', 'robotframework-mongodb-bson-library', 'MongoDBBSONLibrary'],
                     package_dir={'': 'src'},
                     packages=['MongoDBBSONLibrary'],
                     include_package_data=True,
                     install_requires=requirements,
                     zip_safe=False,
                     classifiers=CLASSIFIERS.splitlines(),
                     test_suite='tests',
                     tests_require=test_requirements
                     )


if __name__ == "__main__":
    main()
