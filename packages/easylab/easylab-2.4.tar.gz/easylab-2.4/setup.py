# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['easylab']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'easylab',
    'version': '2.4',
    'description': 'Offers simple solutions for challenges that can be encountered in the psychology labs.',
    'long_description': "[![PyPI version](https://badge.fury.io/py/easylab.svg)](https://badge.fury.io/py/easylab)\n[![pages-build-deployment](https://github.com/altunenes/easylab/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/altunenes/easylab/actions/workflows/pages/pages-build-deployment)\n[![Downloads](https://pepy.tech/badge/easylab)](https://pepy.tech/project/easylab)\n\n#### EasyLab\n\nOffers simple solutions with GUI. From a folder, it can resize images, change their extensions, applies spatial frequencies, and remove backgrounds...\n\n#### Purpose of the project\n\n+ The purpose of the project is to offer simple solutions to solve some of the problems that arise when working with big image datasets.\n+ The project is a work in progress, and it is not finished yet. Since it offers GUI, it is very practical to use it.\n\n#### Features\n\n+ Resize images\n+ Change extension\n+ Apply spatial frequencies (low pass, high pass with Butterworth filter)\n+ Apply Gaussian blur\n+ Apply grayscale filter (RGB to Gray)\n+ Rename images (with a desired prefix)\n+ Remove background from images (Utilizes deep learning, so it is slow depending on the size of the images)\n+ Apply Histogram Equalization\n+ Apply CFA (Color Filter Array) filter\n\n#### installation\n\n+ Install easylab with pip:\n  ```pip install easylab  ```\n\n#### Usage\n\nit is very simple to use the project.\nFor the open GUI, use the following command:\n```from easylab import easylab```\nthen open the gui with:\n```easylab.easylabgui()```\n\nThis basically starts the GUI. First, select the input folder then select the output folder. Then just select the options you want to apply to the images. Rename images will change all image names from the input folder with the input prefix. Don't forget to add an extension if you use rename option.\n\n#### Javascript\n\nI will also add some javascript to the online version. You can find js demos on the easylab website\n[here]( https://altunenes.github.io/easylab/)\n\n#### E-prime scripts\n\nget the trail list (Image names for the E-Prime) or create a jitter:\nhttps://altunenes.github.io/EasyLab/filenames\n\n#### Contributing\n\nContributions are welcome!\n\n+ Enes Altun [Main Author](https://altunenes.github.io)\n\n### Current look\n\n![easylab.png](./docs/images/easylab.png)",
    'author': 'altunenes',
    'author_email': 'enesaltun2@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/altunenes/EasyLab',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
