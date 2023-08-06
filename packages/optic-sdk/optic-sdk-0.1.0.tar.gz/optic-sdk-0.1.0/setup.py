# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['optic']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'optic-sdk',
    'version': '0.1.0',
    'description': 'Python SDK for Optic',
    'long_description': 'Optic Python Sdk\n\n<!-- Badges -->\n[![Build status](https://github.com/silentninja/optic-python/actions/workflows/run_tests.yml/badge.svg)](https://github.com/silentninja/optic-python/actions/workflows/run_tests.yml)\n\nThe code library standardizing data capture for [Optic](https://www.useoptic.com) in Python applications. We have a [list of middleware available for some frameworks](https://github.com/silentninja/optic-python), if we are missing the framework [join our community](https://useoptic.com/docs/community/) and suggest the next framework or develop it with us.\n\n## Requirements\n\nThe library requires `@useoptic/cli` to be installed, instructions on installing it are available [https://www.useoptic.com/docs/](https://www.useoptic.com/docs/).\n\n## Install\n\n```sh\npip install optic-sdk\n```\n\n## Usage\n\nThe library provides apis to interact with optic cli. This library does not provide ecs converters and should be used\nalong with framework specific optic libraries\n\n### Configuration\n\nEnvironment variables can also be used to set the values.\n\n- `ENABLE`: `boolean` (defaults to `True`) Programmatically control if capturing data and sending it to Optic\n- `UPLOAD_URL`: `string` (defaults to `os.environ[\'OPTIC_LOGGING_URL\']`) The URL to Optics capture URL, if left blank it\n  will expect `OPTIC_LOGGING_URL` environment variable set by the Optic CLI\n- `CONSOLE`: `boolean` (defaults to `False`) Send to stdout/console for debugging\n- `framework`: `string`  Additional information to inform Optic of where it is capturing information\n- `LOG`: `boolean` (defaults to `False`) Send to log file\n- `LOG_PATH`: `boolean` (defaults to `./optic.log`) Log file path\n- `LOCAL`: `boolean` (defaults to `True`) Send to optic cli\n\n### Example\n\n        from optic import OpticConfig, Optic\n        def send_to_optic_cli(ecs_object):\n            """\n            ecs_object: Json serializble ecs object\n            """\n            config = OpticConfig(framework="<insert name>", CONSOLE=True)\n            optic = Optic(config)\n            optic.send_to_local_cli(ecs_object) //send to optic cli\n            optic.send_to_file(ecs_object) //save to file\n            optic.send_to_console(ecs_object) //send to stdout\n\n## License\nThis software is licensed under the [MIT license](../LICENSE).\n',
    'author': 'Mukesh',
    'author_email': 'mmukesh95@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/silentninja/optic-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
