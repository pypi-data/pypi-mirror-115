# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['reg2es', 'reg2es.models', 'reg2es.presenters', 'reg2es.views']

package_data = \
{'': ['*']}

install_requires = \
['elasticsearch>=7.7.1,<8.0.0',
 'importlib_metadata>=4.6.1,<5.0.0',
 'libregf-python>=20210615,<20210616',
 'orjson>=3.6.0,<4.0.0',
 'tqdm>=4.46.1,<5.0.0',
 'urllib3>=1.26.5,<2.0.0']

entry_points = \
{'console_scripts': ['reg2es = reg2es.views.Reg2esView:entry_point',
                     'reg2json = reg2es.views.Reg2jsonView:entry_point']}

setup_kwargs = {
    'name': 'reg2es',
    'version': '1.0.1',
    'description': 'A library for fast import of Windows NT Registry(REGF) into Elasticsearch.',
    'long_description': '# reg2es\n\n[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)\n[![PyPI version](https://badge.fury.io/py/reg2es.svg)](https://badge.fury.io/py/reg2es)\n[![Python Versions](https://img.shields.io/pypi/pyversions/reg2es.svg)](https://pypi.org/project/reg2es/)\n\n![reg2es logo](https://gist.githubusercontent.com/sumeshi/c2f430d352ae763273faadf9616a29e5/raw/bd51b2539d8bb639d4f630ef13639706bed1f905/reg2es.svg)\n\nA library for fast import of Windows NT Registry(REGF) into Elasticsearch.  \nreg2es uses C library [libregf](https://github.com/libyal/libregf).\n\n\n## Usage\n\nWhen using from the commandline interface:\n\n```bash\n$ reg2es /path/to/your/file.DAT\n```\n\nWhen using from the python-script:\n\n```python\nfrom reg2es import reg2es\n\nif __name__ == \'__main__\':\n  filepath = \'/path/to/your/file.DAT\'\n  reg2es(filepath)\n```\n\n### Arguments\n\nreg2es supports importing from multiple files.\n\n```bash\n$ reg2es NTUSER.DAT SYSTEM SAM\n```\n\nAlso, possible to import recursively from a specific directory.\n\nNote: In this case, the filename will not be checked, please check for unnecessary files before execute.\n\n```bash\n$ tree .\nregfiles/\n  ├── NTUSER.DAT\n  ├── NTUSER.MAN\n  ├── SAM\n  └── subdirectory/\n    ├── SOFTWARE\n    └── subsubdirectory/\n      ├── SYSTEM\n      └── UsrClass.dat\n\n$ reg2es /regfiles/ # The Path is recursively expanded to file1~6.reg.\n```\n\n### Options\n\n```\n--version, -v\n\n--help, -h\n\n--quiet, -q\n  Flag to suppress standard output\n  (default: False)\n\n--host:\n  ElasticSearch host address\n  (default: localhost)\n\n--port:\n  ElasticSearch port number\n  (default: 9200)\n\n--index:\n  Index name of Import destination\n  (default: reg2es)\n\n--scheme:\n  Scheme to use (http, or https)\n  (default: http)\n\n--pipeline\n  Elasticsearch Ingest Pipeline to use\n  (default: )\n\n--login:\n  The login to use if Elastic Security is enable\n  (default: )\n\n--pwd:\n  The password linked to the login provided\n  (default: )\n\n--fields-limit\n  index.mapping.total_fields.limit settings\n  (default: 10000)\n```\n\n### Examples\n\nWhen using from the commandline interface:\n\n```\n$ reg2es /path/to/your/file.dat --host=localhost --port=9200 --index=foobar\n```\n\nWhen using from the python-script:\n\n```py\nif __name__ == \'__main__\':\n    reg2es(\'/path/to/your/file.dat\', host=localhost, port=9200, index=\'foobar\')\n```\n\nWith the Amazon Elasticsearch Serivce (ES):\n\n```\n$ reg2es /path/to/your/file.dat --host=example.us-east-1.es.amazonaws.com --port=443 --scheme=https --index=foobar\n```\n\nWith credentials for Elastic Security:\n\n```\n$ reg2es /path/to/your/file.dat --host=localhost --port=9200 --index=foobar --login=elastic --pwd=******\n```\n\nNote: The current version does not verify the certificate.\n\n\n## Appendix\n\n### Reg2json\n\nExtra feature. :sushi: :sushi: :sushi:\n\nConvert from Windows NT Registry(REGF) to json file.\n\n```bash\n$ reg2json /path/to/your/file.DAT /path/to/output/target.json\n```\n\nConvert from Windows NT Registry(REGF) to Python dict object.\n\n```python\nfrom reg2es import reg2json\n\nif __name__ == \'__main__\':\n  filepath = \'/path/to/your/file.DAT\'\n  result: dict = reg2json(filepath)\n```\n\n## Output Format\n\nThe structures is not well optimized for searchable with Elasticsearch. I\'m waiting for your PR!!\n\n```json\n{\n  "ROOT": {\n    "AppEvents": {\n      "meta": {\n        "last_written_time": "2015-10-30T07:24:57.814133"\n      },\n      "EventLabels": {\n        "meta": {\n          "last_written_time": "2015-10-30T07:25:51.735838"\n        },\n        "Default": {\n          "meta": {\n            "last_written_time": "2015-10-30T07:24:57.861009"\n          },\n          "_": {\n            "type": 1,\n            "identifier": "REG_SZ",\n            "size": 26,\n            "data": "Default Beep"\n          },\n          "DispFileName": {\n            "type": 1,\n            "identifier": "REG_SZ",\n            "size": 34,\n            "data": "@mmres.dll,-5824"\n          }\n        },\n        "ActivatingDocument": {\n          "meta": {\n            "last_written_time": "2015-10-30T07:24:57.861009"\n          },\n          "_": {\n            "type": 1,\n            "identifier": "REG_SZ",\n            "size": 40,\n            "data": "Complete Navigation"\n          },\n          "DispFileName": {\n            "type": 1,\n            "identifier": "REG_SZ",\n            "size": 40,\n            "data": "@ieframe.dll,-10321"\n          }\n        }\n        ...\n      }\n    }\n  }\n}\n```\n\n## Installation\n\n### via PyPI\n```\n$ pip install reg2es\n```\n\n## Known Issues\n\n```\nelasticsearch.exceptions.RequestError: RequestError(400, \'illegal_argument_exception\', \'Limit of total fields [1000] in index [reg2es] has been exceeded\')\n```\n\nWindows NT Registry has a large number of elements per document and is caught in the initial value of the limit.\nTherefore, please use the --fields-limit(default: 10000) option to remove the limit.\n\n```\n$ reg2es --fields-limit 10000 NTUSER.DAT\n```\n\n## Contributing\n\n[CONTRIBUTING](https://github.com/sumeshi/reg2es/blob/master/CONTRIBUTING.md)\n\nThe source code for reg2es is hosted at GitHub, and you may download, fork, and review it from this repository(https://github.com/sumeshi/reg2es).\nPlease report issues and feature requests. :sushi: :sushi: :sushi:\n\n## License\n\nreg2es is released under the [MIT](https://github.com/sumeshi/reg2es/blob/master/LICENSE) License.\n\nPowered by [libregf](https://github.com/libyal/libregf).\n',
    'author': 'sumeshi',
    'author_email': 'j15322sn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sumeshi/reg2es',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
