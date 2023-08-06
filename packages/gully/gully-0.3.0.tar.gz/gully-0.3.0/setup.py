# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['gully']
setup_kwargs = {
    'name': 'gully',
    'version': '0.3.0',
    'description': 'Simple real time data stream manipulation.',
    'long_description': '# Gully\n\nGully is a simple framework for manipulating asynchronous streams of data.\n\n## Installation\n```shell\npip install gully\n```\n\n## Usage\n```python\nimport gully\n\nasync def monitor_stream_using_iterator(stream: gully.Gully):\n    async for item in stream:\n        print(item)\n\nasync def monitor_stream_using_future(stream: gully.Gully):\n    while not stream.done:\n        item = await stream.next\n        print(item)\n\nasync def monitor_stream_observer(stream: gully.Gully):\n    def observer(item):\n        print(item)\n        \n    stream.watch(observer)\n\ndata_stream = gully.Gully()\nfiltered = data_stream.filter(lambda item: item == "foobar")\nmapped = filtered.map(lambda item: item.upper())\n```\n## Documentation\n\n### gully.Gully(stream: Gully = None, limit: int = -1)\n\nGully is a data stream. It can observe other data streams and it can be observed by either data streams or functions.\n\nIt optionally takes a Gully object which it will observe. It also takes a limit, if it is positive the gully will only return that many values, if it is negative the gully will run so long as it is being passed values.\n\nAll gully instances act as async iterators. So they can be used in an async for to observe future values that get pushed into the gully. When the gully stops it will end the iterator stopping the async for.\n\n- `property Gully.done: bool` Is the gully done, either because it reached its limit or was stopped\n\n- `property Gully.next: gully.FutureView` The future that will receive the next value that is pushed into the data stream. This future will change with every pushed value, it will be cancelled if the stream is stopped or reaches its limit. It is a `FutureView` to prevent alterations to the underlying future. \n\n**`method Gully.push(value: Any)`**\n\nPushes a value into the data stream.\n\n**`method DataStream.stop()`**\n\nStops the stream and cancels the next future stopping all watchers.\n\n**`method Gully.watch(callback: Callable[[Any], None])`**\n\nRegisters a function to be called whenever a new value is pushed into the stream. The function may also be a coroutine.\n\n**`method Gully.filter(predicate: Callable[[Any], bool], limit: int = -1) -> FilteredGully`**\n\nCreates a gully that only pushes values that the predicate function allows. The predicate function should return `True` for any value that should be allowed into the stream.\n\n**`method Gully.map(mapping: Callable[[Any], Any], limit: int = -1) -> MappedGully`**\n\nCreates a gully that passes every value pushed to the stream into the mapping function, the returned value will be pushed into the gully.\n\n### gully.FilteredGully(gully.Gully)\n\nA simple filterable gully that inherits from `Gully`. It expects a callable that takes a single argument and that returns a boolean. The callable will be passed each value that\'s being pushed into the gully and if it returns `True` the value will be allowed, if it returns `False` the value will not be pushed and will be ignored.\n\n### gully.MappedGully\n\nA simple mapping gully that inherits from `Gully`. It expects a callable that takes a single argument and that any value. The callable will be passed each value that\'s being pushed into the gully and the value the callable returns will be what gets pushed.\n',
    'author': 'Zech Zimmerman',
    'author_email': 'hi@zech.codes',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ZechCodes/gully',
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
