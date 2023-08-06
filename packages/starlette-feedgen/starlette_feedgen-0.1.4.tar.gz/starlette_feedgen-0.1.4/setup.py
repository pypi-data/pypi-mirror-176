# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['starlette_feedgen']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=22.1.0,<23.0.0', 'starlette>=0.21.0,<0.22.0']

setup_kwargs = {
    'name': 'starlette-feedgen',
    'version': '0.1.4',
    'description': 'Asynchronous RSS/Atom feeds generation for Starlette, adapted from Django syndication feed framework.',
    'long_description': '# Starlette FeedGen\nAsynchronous RSS/Atom feeds generation for [Starlette](https://www.starlette.io/),\nadapted from [Django syndication feed framework](https://docs.djangoproject.com/en/stable/ref/contrib/syndication/).\n\nNote that in version 0.1.4 and higher we support only Python 3.10+ \nand all library classes now provide asynchronous methods. If any of these does not meet your needs\nplease consider using version 0.1.3 of the library.\n\n## Installation\n```sh\npip install starlette-feedgen\n```\n\n## Usage\n\nHere\'s a simple example of handling route `/feed` using `FeedEndpoint` class.\n\n```python\nfrom typing import NamedTuple\nfrom starlette.applications import Starlette\nfrom starlette_feedgen import FeedEndpoint\n\n\nclass FeedItem(NamedTuple):\n    title = \'Hello\'\n    description = \'There\'\n    link = \'http://example.com/article\'\n\n    \napp = Starlette()\n\n\n@app.route(\'/feed\')\nclass Feed(FeedEndpoint):\n    title = \'Example RSS Feed\'\n    description = \'With example item\'\n    link = \'http://example.com\'\n\n    async def get_items(self):\n\n        def item_generator():\n            yield FeedItem()\n\n        return item_generator()\n```\n\nExample RSS Output:\n\n```xml\n<?xml version="1.0" encoding="utf-8"?>\n<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n    <channel>\n        <title>Example RSS Feed</title>\n        <link>http://example.com</link>\n        <description>With example item</description>\n        <atom:link rel="self" href="/feed"></atom:link>\n        <lastBuildDate>Thu, 20 Oct 2022 12:46:17 +0000</lastBuildDate>\n        <item>\n            <title>Hello</title>\n            <link>http://example.com/article</link>\n            <description>There</description>\n            <guid>http://example.com/article</guid>\n        </item>\n    </channel>\n</rss>\n```\n\nNote that `FeedEndpoint` creates a feed generator object `Rss201rev2Feed` under the hood.\nYou can explicitly import a feed generator class and work with it, for example:\n\n```python\nimport aiofiles\nimport asyncio\nfrom starlette_feedgen.generator import Rss201rev2Feed\n\nfeed = Rss201rev2Feed(\n    title=\'Poynter E-Media Tidbits\',\n    link=\'http://www.poynter.org/column.asp?id=31\',\n    description=\'A group Weblog by the sharpest minds in online media/journalism/publishing.\',\n    language=\'en\',\n)\n\nfeed.add_item(\n    title=\'Hello\',\n    link=\'http://www.holovaty.com/test/\',\n    description=\'Testing.\'\n)\n\n\nasync def write_to_file():\n    async with aiofiles.open(\'test.rss\', \'w\') as f:\n        await feed.write(f, \'utf-8\')\n\nasyncio.run(write_to_file())\n```\n\nRSS Output:\n```xml\n<?xml version="1.0" encoding="utf-8"?>\n<rss version="2.0"\n\txmlns:atom="http://www.w3.org/2005/Atom">\n\t<channel>\n\t\t<title>Poynter E-Media Tidbits</title>\n\t\t<link>http://www.poynter.org/column.asp?id=31</link>\n\t\t<description>A group Weblog by the sharpest minds in online media/journalism/publishing.</description>\n\t\t<language>en</language>\n\t\t<lastBuildDate>Thu, 20 Oct 2022 13:24:50 +0000</lastBuildDate>\n\t\t<item>\n\t\t\t<title>Hello</title>\n\t\t\t<link>http://www.holovaty.com/test/</link>\n\t\t\t<description>Testing.</description>\n\t\t</item>\n\t</channel>\n</rss>\n```\n\nFor definitions of the different versions of RSS, see:\nhttps://web.archive.org/web/20110718035220/http://diveintomark.org/archives/2004/02/04/incompatible-rss',
    'author': 'Arseny Gabdullin',
    'author_email': 'a.gabdullin@tinkoff.ru',
    'maintainer': 'Andrey Tsvetkov',
    'maintainer_email': 'an.a.tsvetkov@tinkoff.ru',
    'url': 'https://github.com/tinkoffjournal/starlette-feedgen',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
