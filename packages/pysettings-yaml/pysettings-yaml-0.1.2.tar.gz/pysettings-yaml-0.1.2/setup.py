# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysettings_yaml', 'pysettings_yaml.providers']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'deepmerge>=1.1.0,<2.0.0',
 'funcy>=1.17,<2.0',
 'pydantic>=1.10.2,<2.0.0',
 'python-decouple>=3.6,<4.0',
 'split-settings>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'pysettings-yaml',
    'version': '0.1.2',
    'description': 'Settings library for human beings',
    'long_description': '# Pysettings YAML\n\nThis library extends over the concepts of [Decouple](https://github.com/henriquebastos/python-decouple/) \nand [Split Settings](https://django-split-settings.readthedocs.io/en/latest/)\nto create a library that is simple to use and expresses your settings in a\nyaml file for higher expressivity.\n\n## Installation\n\n```\npip install pysettings-yaml\n```\n\n## Usage\n\nDefine a YAML file with the definition of your settings, for example, \na `settings.yaml` in the same path as your settings module:\n\n```yaml\nsettings:\n  SAMPLE_SETTING_BOOL:  # Each entry inside the settings section is the name of your setting\n    origins:\n      - name: env\n      - name: direct\n        value: true\n  SAMPLE_SETTING_STR:\n    origins:\n      - name: direct\n        value: banana\n      - name: env\n```\n\nThen you can use this file like this in a `settings.py`:\n\n```python\nfrom split_settings.tools import optional\nfrom pathlib import Path\n\nfrom pysettings_yaml import get_config\n\nBASE_DIR = Path(__file__).parent\n\nsetting_files = [\n    BASE_DIR / "settings.yaml",\n]\n\n\nconfig = get_config(setting_files)\n\nSAMPLE_SETTING_BOOL = config("SAMPLE_SETTING_BOOL", cast=bool)\nSAMPLE_SETTING_STR = config("SAMPLE_SETTING_STR")\n\nprint(SAMPLE_SETTING_BOOL)\nprint(SAMPLE_SETTING_STR)  # This will print banana\n```\n\nBy default the library supports two origin names: `env` (to receive the value of your setting using the _decouple_ library)\nor `direct` (to provide a constant value), but you can add your own providers easily\n(refer to the "Adding custom providers" section).\n\nOrigin are evaluated in strict order. In those examples, `SAMPLE_SETTING_BOOL`\nwill evaluate first the `env` origin and, if that value is `None`, it will\nprocess the next origin, which would be `direct`. In contrast, for `SAMPLE_SETTING_STR`,\nthe first origin is the `direct` origin. Since direct can never return `None`,\nthe env origin will never be evaluated.\n\n\n## Overriding settings\n\nYou can define several setting files to be processed in order.\nAll of them will be merged together, so any subsequent setting file\nwill override the settings with the same name defined in a previous file\nof the list. Very useful if you need to define different origins\nfor your settings depending on your deployment environment:\n\n```python\nfrom split_settings.tools import optional\nfrom pathlib import Path\nimport os\n\nfrom pysettings_yaml import get_config\nENVIRONMENT = os.environ.get("ENVIRONMENT", "dev")\n\nBASE_DIR = Path(__file__).parent\n\nsetting_files = [\n    BASE_DIR / "settings.yaml",\n    BASE_DIR / f"settings.{ENVIRONMENT}.yaml",\n    optional(BASE_DIR / "settings.nonexistent.yaml")\n]\n\n\nconfig = get_config(setting_files)\n\nSAMPLE_SETTING_BOOL = config("SAMPLE_SETTING_BOOL", cast=bool)\nSAMPLE_SETTING_STR = config("SAMPLE_SETTING_STR")\n```\n\nAny path wrapped with the `optional` function will not raise an\nexception should that file not exist in the path you specify.\n\n## Adding custom providers\n\nIf you need other providers (for example for getting your settings from a vault\nlike Amazon SSM) you can implement your own providers like this:\n\n```python\nfrom typing import Union, Optional\n\nfrom pysettings_yaml.providers.interfaces import SettingsProvider, OriginModel, NoValue\n\n\nclass AWSModel(OriginModel):\n    path: str\n    decrypt: bool\n\n\nclass SampleAWSSettingsProvider(SettingsProvider):\n    name = "aws"\n    schema = AWSModel\n\n    def get(\n        self, setting_name: str, origin_data: AWSModel\n    ) -> Union[Optional[str], NoValue]:\n        return f"path: {origin_data.path}, decrypt: {origin_data.decrypt}"\n\n```\n\nJust make sure to:\n* Provide the `name` and a pydantic `schema`\n* Implement the `get` method\n\nThen you can obtain your config providing your `SettingProvider` and use it in your yaml:\n\n```python\nconfig = get_config(setting_files, additional_providers=[SampleAWSSettingsProvider()])\n```\n\n```yaml\nsettings:\n  SAMPLE_SETTING:\n    origins:\n      - name: aws\n        path: some/path\n        decrypt: true\n      - name: env\n```\n',
    'author': 'David',
    'author_email': 'davigetto@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Rydra/pysettings-yaml',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
