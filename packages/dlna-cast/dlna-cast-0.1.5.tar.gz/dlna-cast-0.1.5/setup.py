# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dlna_cast']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.4.0,<0.5.0',
 'python-dotenv[cli]>=0.21.0,<0.22.0',
 'upnpclient>=1.0.3,<2.0.0']

entry_points = \
{'console_scripts': ['dlna-cast = dlna_cast.main:main']}

setup_kwargs = {
    'name': 'dlna-cast',
    'version': '0.1.5',
    'description': 'A cross-platform command-line tool that casts screen and media file to remote DLNA device.',
    'long_description': '# dlna-cast\nA cross-platform command-line tool that casts screen and media file to remote DLNA device.\n\n## Introduction\n`dlna-cast` uses `ffmpeg` to capture screen and audio, then convert them into HLS streams which could be served by a simple HTTP server. The HLS url will be send to the selected device via uPnP protocol and the screen will be casted to the remote device (smart TV, typically).\n\nThis tool is supposed to be cross-platform but currently I don\'t have a Linux or MacOS device at hand so it can only run on Windows now. It won\'t be hard to support other platforms though, as there is no platform specific dependencies.\n\nHLS is chosen just because it is easy to implement. But the problem of HLS is its high latency (up to 5s or more) so it\'s definitely not for scenarios that require low latency (presentation for example). But as a trade-off the streaming quality exceeds a lot of software-based screen-casting solutions (Lebocast for example) that have been tested by myself, which make it pretty good to stream music or video playing on your PC to the supported TV.\n\n## Install\n```bash\npip install dlna-cast\n```\nPlease ensure your Python is 3.7 or above.\n\n### Install ffmpeg\nYou can install `ffmpeg` by compiling from source code, or just download the prebuild binary from https://ffmpeg.org/download.html\n\nYou need to ensure the `ffmpeg` command can be found in the `PATH` environment variable, or else you need to set `FFMPEG_BIN` or `FFMPEG_HOME` to let `dlna-cast` know where to find the command. \n\n`dlna-cast` supports reading the environment variable from `.env` file.  You can create a `.env` file under the folder you are gonna run the `dlna-cast` command with the following content.\n\n```bash\nFFMPEG_BIN=D:\\ffmpeg\\ffmpeg.exe\n# or\nFFMPEG_HOME=D:\\ffmpeg\n```\n\nYou can also use the `dotenv set` command to update the `.env` file and use the `dotenv list` to check result.\n\n```bash\ndotenv set FFMPEG_HOME "D:\\ffmpeg"\ndotenv list\n```\n\n### Install ScreenCapturerRecorder on Windows\nThough `ffmpeg` is shipped with `gdigrab` to capture screens on Windows, its performance is terrible when frame rate is high. `dlna-cast` uses ScreenCapturerRecorder for the sake of performance. You need to [download](https://github.com/rdp/screen-capture-recorder-to-video-windows-free/releases) and install it before starting to cast.\n\n## Get Started\nBefore you start to stream your screen to remote devices that support DLNA protocol, you need to discover available devices in your LAN by running the following command.\n\n```bash\ndlna-cast list_dlna_devices\n# You will see the output if supported devices are found\nHuaweiPro\nLebocast\n```  \n\nAnd now you can cast your screen to one of the found devices by running the following command.\n```bash\ndlna-cast screen --dlna_device HuaweiPro\n``` \n\nOr you can also set `DLNA_DEVICE` in the `.env` file so that you can skip to set `--dlna_device` next time.\n\n```bash\ndotenv set DLNA_DEVICE HuaweiPro\ndlna-cast screen\n```\n\nTo stop casting just press `Ctrl+C`. \n\n## TODO\n[ ] Support cast media file.\n[ ] Optimize devices discover.\n[ ] Optimize latency.\n[ ] Cross platform support.\n',
    'author': 'weihong.xu',
    'author_email': 'xuweihong.cn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
