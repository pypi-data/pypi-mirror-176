# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['setfitonnx']

package_data = \
{'': ['*']}

install_requires = \
['joblib>=1.2.0,<2.0.0',
 'loguru>=0.6.0,<0.7.0',
 'onnx>=1.12.0,<2.0.0',
 'onnxruntime>=1.13.1,<2.0.0',
 'sclblonnx>=0.1.14,<0.2.0',
 'setfit>=0.4.1,<0.5.0',
 'skl2onnx>=1.13,<2.0']

setup_kwargs = {
    'name': 'setfitonnx',
    'version': '0.1.0',
    'description': 'Package to pack setfit model to onnx format',
    'long_description': '# SetFitONNX\n## Export the setfit model to ONNX format\n\n\n## Features\n\n- Mean Pooling Layer to ONNX Graph\n- Single ONNX Model combining both the sentence transformer & classification head\n\n## Installation\n```sh\npip install setfitonnx\n```\n## How to \n```python\nfrom setfitonnx import convert_onnx\n\n# Setfit Model directory\nmodel_path = "/home/mysetfit-model"\n# ONNX Output directory\noutput_dir = "/home/setfit-onnx-model"\n# Convert to ONNX\nconvert_onnx(model_path=model_path,output_dir=output_dir)\n\n```\n\n## License\n\nMIT',
    'author': 'Vimal Babu',
    'author_email': 'personal.vimal@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vimal-b/setfitonnx',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
