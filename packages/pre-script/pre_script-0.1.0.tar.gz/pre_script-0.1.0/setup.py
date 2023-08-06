# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pre_script']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pre-script',
    'version': '0.1.0',
    'description': 'Util for executing a custom script before running any python application without modifying the last one',
    'long_description': '# Pre Script\n\nUtil for executing a custom script before running any python application or script without modifying the last one.\n\nYou may treat it as application pre-start hook.\n\n## Use cases\n- patching log configs for a legacy application (sometimes it\'s pretty hard)\n- auto-executing `docker-compose.yml` before running the application\n- patching the application module (sometimes usefull for debugging)\n- any case where you need to inject some temporary logic without modifying the application code base\n\n## Installation\n\n```console\n$ pip install pre-script\n```\n\n## Example\n\n```console\n$ echo PRE_SCRIPT_ENABLED=1\n$ echo \'print("hello from pre-script")\' > .pre-script.py\n$ echo \'print("hello from app")\' > app.py\n```\n\n```console\n$ python app.py\n$ hello from pre-script\n$ hello from app\n```\n\nIf required, the script name can be changed via `PRE_SCRIPT_FILE` environment variable.\n\n## License\n\nDistributed under the terms of the [MIT license][license],\n_Pre Script_ is free and open source software.\n',
    'author': 'Andrey Torsunov',
    'author_email': 'andrey.torsunov@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/gtors/pre-script',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
