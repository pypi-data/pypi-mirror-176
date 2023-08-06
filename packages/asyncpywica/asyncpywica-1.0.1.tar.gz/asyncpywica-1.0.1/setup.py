# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wica']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.0,<0.24.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'asyncpywica',
    'version': '1.0.1',
    'description': 'A simple async python API to access wica-http SSE.',
    'long_description': '# Py-Wica Async\n#### Table of Contents\n- [Introduction](#introduction)\n- [Installation](#installation)\n- [Quick-start Guid](#quick-start-guide)\n- [Documentation](#documentation)\n- [Dependencies](#dependencies)\n- [Contribute](#contribute)\n- [Project Changes and Tagged Releases](#project-changes-and-tagged-releases)\n- [Developer Notes](#developer-notes)\n- [Contact](#contact)\n\n# Introduction\nThis project/package aims to provide a simple python interface to the wica-http server.\nCheck out the main branch to get the blocking version of the package\n\n# Installation\nInstall with pip\n```bash\npip install py-wica-async\n```\n# Quick-start Guide\n```python\nimport asyncio\nimport time\n\nfrom py-wica-aync import AsyncWicaStream\n\n\nasync def async_simple_example():\n    """A simple example of how to use AsyncWicaStream. Run it in main by uncommenting it! """\n\n    wica_stream = AsyncWicaStream(base_url="http://student08/ca/streams", channels=["MMAC3:STR:2"])\n\n    async def run_stream():\n        await wica_stream.create()\n        async for message in wica_stream.subscribe():\n            print(message)\n\n    async def stop_stream():\n        await asyncio.sleep(10)\n        print(await wica_stream.destroy())\n\n    await asyncio.gather(run_stream(), stop_stream())\n\n\nasync def async_multistream_example():\n    """ An example of how to run multiple streams at once.\n\n    Use aiostream to run it! Run it by uncommenting it in main.\n    """\n    from aiostream import stream\n    streams = []\n    async def run_streams():\n        for _ in range(10):\n            wica_stream = AsyncWicaStream(base_url="http://student08/ca/streams", channels=["MMAC3:STR:2"])\n            streams.append(wica_stream)\n            await wica_stream.create()\n\n        print("Doing someting else before starting the stream...")\n        await asyncio.sleep(5)\n\n        subscribed_streams = []\n\n        for wica_stream in streams:\n            print(f"Subscribing to stream {wica_stream.id}")\n            subscribed_streams.append(wica_stream.subscribe())\n\n\n        combine = stream.merge(*subscribed_streams)\n        async with combine.stream() as streamer:\n            async for item in streamer:\n                print(item)\n                continue\n\n\n    async def stop_streams():\n        await asyncio.sleep(25)\n        for wica_stream in streams:\n            print(await wica_stream.destroy())\n\n\n    await asyncio.gather(run_streams(), stop_streams())\n\n\nasync def main():\n    await async_simple_example()\n    #await async_multistream_example()\n\n\nif __name__ == "__main__":\n    asyncio.run(main())\n\n```\n\n# Documentation\nCurrent Features:\n* Custom Client to handle be able to extract last line of SSE with timestamp and message type.\n* Simple functions to create, delete and subscribe to streams\n* Fully Async (blocking versions available in main branch)\n\nCheck out the wiki for mor info!\n\n# Dependencies\n* [httpx](https://github.com/encode/httpx/)\n\n# Contribute\nTo contribute, simply clone the project.\n\n# Project Changes and Tagged Releases\n* See the Changelog file for further information\n* project releases are available in pypi\n\n# Developer Notes\nCurrently None\n\n# Contact\nIf you have any questions pleas contract \'niklas.laufkoetter@psi.ch\'',
    'author': 'Niklas Laufkoetter',
    'author_email': 'niklas.laufkoetter@psi.ch',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
