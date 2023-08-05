# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['manim_voiceover', 'manim_voiceover.services']

package_data = \
{'': ['*']}

install_requires = \
['manim>=0.16.0.post0,<0.17.0',
 'mutagen>=1.46.0,<2.0.0',
 'pydub>=0.25.1,<0.26.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'sox>=1.4.1,<2.0.0']

entry_points = \
{'manim.plugins': ['manim_voiceover = manim_voiceover']}

setup_kwargs = {
    'name': 'manim-voiceover',
    'version': '0.1.2',
    'description': 'Manim plugin for all things voiceover',
    'long_description': '# Manim Voiceover\n\n<p>\n    <a href="https://github.com/ManimCommunity/manim-voiceover/workflows/Build/badge.svg"><img src="https://github.com/ManimCommunity/manim-voiceover/workflows/Build/badge.svg" alt="Github Actions Status"></a>\n    <a href="https://pypi.org/project/manim_voiceover/"><img src="https://img.shields.io/pypi/v/manim_voiceover.svg?style=flat&logo=pypi" alt="PyPI Latest Release"></a>\n    <a href="https://pepy.tech/project/manim_voiceover"><img src="https://pepy.tech/badge/manim_voiceover/month?" alt="Downloads"> </a>\n    <a href="https://manim_voiceover.readthedocs.io/en/latest/?badge=latest"><img src="https://readthedocs.org/projects/manim_voiceover/badge/?version=latest" alt="Documentation Status"></a>\n    <a href="https://github.com/ManimCommunity/manim-voiceover/blob/main/LICENSE"><img src="https://img.shields.io/github/license/ManimCommunity/manim-voiceover.svg?color=blue" alt="License"></a>\n    <a href="https://manim.community/discord"><img src="https://dcbadge.vercel.app/api/server/qY23bthHTY?style=flat" alt="Discord"></a>\n</p>\n\nManim Voiceover is a [Manim](https://manim.community) plugin for all things voiceover:\n\n- Add voiceovers to Manim videos _directly in Python_ without having to use a video editor.\n- Develop an animation with an auto-generated AI voice without having to re-record and re-sync the audio.\n- Record a voiceover and have it stitched back onto the video instantly. (Note that this is not the same as AI voice cloning)\n\nHere is a demo:\n\nhttps://user-images.githubusercontent.com/2453968/198145393-6a1bd709-4441-4821-8541-45d5f5e25be7.mp4\n\nCurrently supported TTS services:\n\n- [Azure Text to Speech](https://azure.microsoft.com/en-us/services/cognitive-services/text-to-speech/) (Recommended)\n- [gTTS](https://github.com/pndurette/gTTS/)\n- [pyttsx3](https://github.com/nateshmbhat/pyttsx3)\n\n[Check out the documentation for more details.](https://voiceover.manim.community/)\n\n## Installation\n\n[Installation instruction in Manim Voiceover docs.](https://voiceover.manim.community/en/latest/installation.html)\n\n## Get started\n\n[Check out the docs for getting started with Manim Voiceover.](https://voiceover.manim.community/en/latest/quickstart.html)\n\n',
    'author': 'The Manim Community Developers',
    'author_email': 'contact@manim.community',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ManimCommunity/manim-voiceover',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
