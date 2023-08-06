# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pennsieve2', 'pennsieve2.protos']

package_data = \
{'': ['*']}

install_requires = \
['protobuf>=3.12.0']

extras_require = \
{':extra == "dev"': ['grpcio>=1.50', 'tqdm>=4.64'],
 'dev': ['black>=20.8b1', 'codecov>=2.0.8', 'pytest>=4.4']}

setup_kwargs = {
    'name': 'pennsieve2',
    'version': '0.0.5',
    'description': 'Pennsieve Python Client',
    'long_description': 'Pennsieve Python client (pennsieve2)\n================\n[![PyPI Latest Release](https://img.shields.io/pypi/v/pennsieve2.svg)](https://pypi.org/project/pennsieve2/)\n[![pypi](https://img.shields.io/pypi/pyversions/pennsieve2.svg)](https://pypi.org/project/pennsieve2/)\n[![Package Status](https://img.shields.io/pypi/status/pennsieve2.svg)](https://pypi.org/project/pennsieve2/)\n[![License](https://img.shields.io/pypi/l/pennsieve2.svg)](https://github.com/Pennsieve/pennsieve-agent-python/blob/main/LICENSE)\n[![Coverage](https://codecov.io/github/pennsieve/pennsieve-agent-python/coverage.svg?branch=main)](https://codecov.io/gh/pennsieve/pennsieve-agent-python)\n\nPython client and command line tool for Pennsieve (pennsieve2).\n\n\nPrerequisites\n-------------\nIn order to use this Python library to upload files to Pennsieve, please follow the instruction on installing and setting up Pennsieve agent, which could be found in the documentation.\n\n\nInstallation\n------------\n\nTo install, run:\n\n```bash\n    pip install -U pennsieve2\n```\n\nTo install specific dev version, run:\n```bash\n    pip install -U --index-url https://test.pypi.org/simple/ pennsieve2==0.0.5.post6\n```\n\nContributions\n--------------\n\nTo update gRPC python files, execute from the src folder:\n\n```bash\n    rm src/pennsieve2/protos/agent_pb2*\n    cd src\n    python3.9 -m grpc_tools.protoc --python_out=. -I. --grpc_python_out=. pennsieve2/protos/agent.proto\n```\nNotice, this command does not produce a valid agent_pb2.py file when executed for Python3.10 or formatted by black - it does not use reflection and is reported as error for Flake8.\n\n\nTo create a package and upload it to PyPI, first update the package version in the pennsieve2/__init__.py, then execute:\n\n```bash\n    python -m build\n    # For testing:\n    twine upload -r testpypi dist/*\n    # For production:\n    twine upload dist/*\n```\n\nDocumentation\n-------------\n\nClient and command line documentation can be found on [Pennsieve’s documentation website](https://docs.pennsieve.io/docs/uploading-files-programmatically).\n\n',
    'author': 'Patryk Orzechowski',
    'author_email': 'patryk@upenn.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
