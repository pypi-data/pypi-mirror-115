# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['a9s', 'a9s.aws_resources', 'a9s.components']

package_data = \
{'': ['*']}

install_requires = \
['attrdict>=2.0.1,<3.0.0',
 'blessed>=1.18.0,<2.0.0',
 'boto3>=1.17.87,<2.0.0',
 'cached-property>=1.5.2,<2.0.0',
 'colored>=1.4.2,<2.0.0',
 'pydash>=5.0.2,<6.0.0',
 'pyperclip>=1.8.2,<2.0.0']

entry_points = \
{'console_scripts': ['a9s = a9s.main:main']}

setup_kwargs = {
    'name': 'a9s',
    'version': '0.7.0',
    'description': 'Cli tool for navigation in Amazon AWS services. Highly inspired from k9s',
    'long_description': '# a9s\n\n![](https://img.shields.io/github/v/release/IamShobe/a9s) ![](https://img.shields.io/github/workflow/status/IamShobe/a9s/Create%20and%20publish%20a%20Python%20package?label=pypi%20build) ![](https://img.shields.io/github/workflow/status/IamShobe/a9s/Create%20and%20publish%20a%20Docker%20image?label=docker%20build)  \nCli tool for easily navigating in AWS services.  \nHighly inspired from [k9s](https://github.com/derailed/k9s). \n\n\n## How to install\n\n```shell\npip install a9s\n```\n\n### Docker build\n\n```shell\ndocker build . -t a9s\ndocker run -v ~/.aws/:/root/.aws -it --rm a9s\n```\n\n### Running docker from cloud\n\n```shell\ndocker run -v ~/.aws/:/root/.aws -it --rm ghcr.io/iamshobe/a9s\n```\n\n\n### How to develop\n\n#### Running mock server\nInstall poetry env:\n```bash\npoetry install\n```\nStart dev server:\n```bash\npoetry run moto_server -p 54321\n```\nRun mock data:\n```bash\npoetry run python -m mocked_env.main\n```\n\n#### Running mock server with docker-compose\n```bash\ndocker-compose -f mocked_env/docker-compose.yaml up --build\n```\n\n#### Running a9s in with mocked server\nRun a9s in local mode (connects to mock server on port 54321):\n```bash\nLOCAL=true poetry run a9s\n```\n\n## Goals\n\n### Services\n- [X] s3 support\n- [X] route53 support\n- [ ] EC2 support\n- [ ] ELB support\n- [ ] Cloudfront support\n\n\n### Features\n- [X] responsive tables\n- [X] allow to easily switch between services\n- [X] auto-complete commands\n- [X] vim shortcuts support\n- [X] opening files in S3\n- [X] quick yank\n- [ ] smart navigation between services - route53 pointing to ELB etc..\n',
    'author': 'Elran Shefer',
    'author_email': 'elran777@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/IamShobe/a9s',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
