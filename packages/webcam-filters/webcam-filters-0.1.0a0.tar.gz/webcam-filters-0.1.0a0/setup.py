# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['webcam_filters']
install_requires = \
['av>=8.0.3,<9.0.0',
 'mediapipe>=0.8.6,<0.9.0',
 'opencv-contrib-python>=4.5.3,<5.0.0',
 'typer[all]>=0.3.2,<0.4.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0']}

entry_points = \
{'console_scripts': ['webcam-filters = webcam_filters:cli']}

setup_kwargs = {
    'name': 'webcam-filters',
    'version': '0.1.0a0',
    'description': 'Add filters (background blur, etc) to your webcam on Linux',
    'long_description': 'webcam-filters\n==============\n\nAdd filters (background blur, etc) to your webcam on Linux.\n\n\nWhy?\n----\nVideo conferencing applications tend to either lack video effects altogether or\nsupport only a limited set of capabilities on Linux (e.g. Zoom, Google Meets).\n\nGoal here is to provide a virtual webcam via ``v4l2loopback`` with a common\nset of filters that can be used everywhere.\n\nInstallation\n------------\nYou can either use `pipx` or `pip`. Pipx_ is recommend to keep dependencies\nisolated.\n\nLatest stable::\n\n  $ pipx install webcam-filters || pip install --user webcam-filters\n\nLatest pre-release::\n\n  $ pipx install --pip-args "--pre" webcam-filters || pip install --user --pre webcam-filters\n\nGit::\n\n  $ url="git+https://github.com/jashandeep-sohi/webcam-filters.git" pipx install "$url" || pip install --user "$url"\n\n\nv4l2loopback\n------------\n`v4l2loopback` kernel module is required to emulate a virtual webcam. See your\ndistro\'s docs or v4l2loopback_ on how to install and set it up.\n\nYou\'ll probably want to create at least one loopback device (that\'s persistent\non boot)::\n\n  $ sudo tee /etc/modprobe.d/v4l2loopback.conf << "EOF"\n  # /dev/video3\n  options v4l2loopback video_nr=3\n  options v4l2loopback card_label="Virtual Webcam"\n  options v4l2loopback exclusive_caps=1\n  EOF\n  $ sudo modprobe v4l2loopback\n  $ v4l2-ctl --device /dev/video3 --info\n\nUsage\n-----\nPassthrough (no-op)::\n\n  $ webcam-filters --input-dev /dev/video0 --output-dev /dev/video3\n\nBlur background::\n\n  $ webcam-filters --input-dev /dev/video0 --output-dev /dev/video3 --background-blur 50\n\n.. _Pipx: https://github.com/pypa/pipx\n.. _v4l2loopback_: https://github.com/umlaeute/v4l2loopback\n',
    'author': 'Jashandeep Sohi',
    'author_email': 'jashandeep.s.sohi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jashandeep-sohi/webcam-filters',
    'py_modules': modules,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
