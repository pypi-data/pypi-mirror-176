# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['data_processing_library']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'data-processing-library',
    'version': '0.1.1',
    'description': 'Simple data processing library',
    'long_description': "# DataProcessingLibrary\n\nPython port for [Skivsoft.Processor](https://github.com/skivsoft/Skivsoft.Processor)\n\nSimple data processing library.\n\nThe key features are:\n* Easy idea for running tasks step-by-step\n* Synchronous and asynchronous way for executing steps\n* Support SOLID\n\n\n## Example of usage\n\n```Python\nfrom uuid import uuid4\nfrom data_processing_library.processor import AbstractProcessor, Context\nfrom data_processing_library.group import ProcessorGroup\n\n\nclass HelloContext(Context):\n    def __init__(self):\n        self.name = None\n\n    def set_name(self, name: str) -> None:\n        self.name = name\n\n    def get_name(self) -> str:\n        return self.name\n\n\nclass InputName(AbstractProcessor):\n    def execute(self, context: HelloContext):\n        context.set_name(uuid4().hex)\n\n\nclass OutputGreeting(AbstractProcessor):\n    def execute(self, context: HelloContext):\n        print(f'Hello, {context.get_name()}!')\n\n\ndef run_processor():\n    hello_context = HelloContext()\n    steps = [\n        InputName(),\n        OutputGreeting(),\n    ]\n    processor = ProcessorGroup(steps)\n    processor.execute(hello_context)\n\n\nif __name__ == '__main__':\n    run_processor()\n```\n",
    'author': 'DFilyushin',
    'author_email': 'Dmitriy.Filyushin@yandex.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
