Robotframework-MongoDB-Library
==============================

A library for interacting with MongoDB from RobotFramework.

Uses pymongo.

Notes
-----

This is a fork from the library [Robotframework-MongoDB-Library](https://github.com/robotframework-thailand/robotframework-mongodb-library.git)

main change is that the json string parsing will be modified to bson loads method, 
this way all bson functions like (ObjectId, Timestamps ....etc ) will be supported directly without any needs to explicitly parse using bson in robot framwork



License
-------
See LICENSE file for updated license information

Install
-------
You can install by pulling down source and executing the following:

'''
sudo python setup.py install
'''



You can install using pip

'''
pip install robotframework-mongodb-bson-library
'''

# Documentation
For the detail keyword documentation. Go to this following link:

https://momenh.github.io/robotframework-mongodb-bson-library/

- install build tools:

    $ python3 -m pip install --upgrade build

- build dist:

    $ python3 -m build
 
- install twine for upload to:

    $ python3 -m pip install --upgrade twine

- upload dist package:

    $ python3 -m twine upload --repository pypi dist/*
