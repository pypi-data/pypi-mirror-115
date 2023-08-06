# DO NOT EDIT!!! built with `python _building/build_setup.py`
import setuptools
setuptools.setup(
    name="k3awssign",
    packages=["k3awssign"],
    version="0.1.0",
    license='MIT',
    description='A python lib is used for adding aws version 4 signature to request.',
    long_description="# k3awssign\n\n[![Action-CI](https://github.com/pykit3/k3awssign/actions/workflows/python-package.yml/badge.svg)](https://github.com/pykit3/k3awssign/actions/workflows/python-package.yml)\n[![Build Status](https://travis-ci.com/pykit3/k3awssign.svg?branch=master)](https://travis-ci.com/pykit3/k3awssign)\n[![Documentation Status](https://readthedocs.org/projects/k3awssign/badge/?version=stable)](https://k3awssign.readthedocs.io/en/stable/?badge=stable)\n[![Package](https://img.shields.io/pypi/pyversions/k3awssign)](https://pypi.org/project/k3awssign)\n\nA python lib is used for adding aws version 4 signature to request.\n\nk3awssign is a component of [pykit3] project: a python3 toolkit set.\n\n\nThis lib is used to sign a request using aws signature version 4. You\nneed to provide a python dict which represent your request(it typically\ncontains `verb`, `uri`, `args`, `headers`, `body`), and your access key\nand your secret key. This lib will add signature to the request.\n\n\n\n# Install\n\n```\npip install k3awssign\n```\n\n# Synopsis\n\n```python\n\nimport k3awssign\nimport httplib\n\naccess_key = 'your access key'\nsecret_key = 'your secret key'\n\nsigner = k3awssign.Signer(access_key, secret_key)\n\nfile_content = 'bla bla'\nrequest = {\n    'verb': 'PUT',\n    'uri': '/test-bucket/test-key',\n    'args': {\n        'foo2': 'bar2',\n        'foo1': True,\n        'foo3': ['bar3', True],\n    },\n    'headers': {\n        'Host': 'bscstorage.com',\n        'Content-Length': len(file_content),\n    },\n    'body': file_content,\n}\n\nsigner.add_auth(request, sign_payload=True)\n\nconn = httplib.HTTPConnection('ss.bscstorage.com')\nconn.request(request['verb'], request['uri'],\n             request['body'], request['headers'])\nresp = conn.getresponse()\n\n```\n\n#   Author\n\nZhang Yanpo (张炎泼) <drdr.xp@gmail.com>\n\n#   Copyright and License\n\nThe MIT License (MIT)\n\nCopyright (c) 2015 Zhang Yanpo (张炎泼) <drdr.xp@gmail.com>\n\n\n[pykit3]: https://github.com/pykit3",
    long_description_content_type="text/markdown",
    author='Zhang Yanpo',
    author_email='drdr.xp@gmail.com',
    url='https://github.com/pykit3/k3awssign',
    keywords=['python', 'aws'],
    python_requires='>=3.0',

    install_requires=['k3ut>=0.1.15,<0.2'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
    ] + ['Programming Language :: Python :: 3'],
)
