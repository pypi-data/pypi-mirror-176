# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pgjobq', 'pgjobq._migrations']

package_data = \
{'': ['*'], 'pgjobq': ['_sql/*']}

install_requires = \
['anyio>=3.6.1,<3.7.0', 'asyncpg>=0.26.0,<0.27.0']

extras_require = \
{':python_version < "3.8"': ['typing-extensions>=4.3.0,<5.0.0']}

setup_kwargs = {
    'name': 'pgjobq',
    'version': '0.10.0',
    'description': 'PostgreSQL backed job queues',
    'long_description': '# pgjobq\n\nA job queue built on top of Postgres.\n\n## Project status\n\nPlease do not use this for anything other than experimentation or inspiration.\nAt some point I may decide to support this long term (at which point this warning will be removed), but until then this is just a playground subject to breaking changes (including breaking schema changes).\n\n## Purpose\n\nSometimes you have a Postgres database and need a queue.\nYou could stand up more infrastructure (SQS, Redis, etc), or you could use your existing database.\nThere are plenty of use cases for a persistent queue that do not require infinite scalability, snapshots or any of the other advanced features full fledged queues/event buses/job brokers have.\n\n## Features\n\n* Best effort at most once delivery (jobs are only delivered to one worker at a time)\n* Automatic redelivery of failed jobs (even if your process crashes)\n* Low latency delivery (near realtime, uses PostgreSQL\'s `NOTIFY` feature)\n* Low latency completion tracking (using `NOTIFY`)\n* Dead letter queuing\n* Job attributes and attribute filtering\n* Job dependencies (for processing DAG-like workflows or making jobs process FIFO)\n* Persistent scheduled jobs (scheduled in the database, not the client application)\n* Job cancellation (guaranteed for jobs in the queue and best effort for checked-out jobs)\n* Bulk sending and polling to support large workloads\n* Back pressure / bound queues\n* Fully typed async Python client (using [asyncpg])\n* Exponential back off for retries\n* Telemetry hooks for sampling queries with EXPLAIN or integration with OpenTelemetry.\n\nPossible features:\n\n* Reply-to queues and response handling\n\n## Examples\n\n```python\nfrom contextlib import AsyncExitStack\n\nimport anyio\nimport asyncpg  # type: ignore\nfrom pgjobq import create_queue, connect_to_queue, migrate_to_latest_version\n\nasync def main() -> None:\n\n    async with AsyncExitStack() as stack:\n        pool: asyncpg.Pool = await stack.enter_async_context(\n            asyncpg.create_pool(  # type: ignore\n                "postgres://postgres:postgres@localhost/postgres"\n            )\n        )\n        await migrate_to_latest_version(pool)\n        await create_queue("myq", pool)\n        queue = await stack.enter_async_context(\n            connect_to_queue("myq", pool)\n        )\n        async with anyio.create_task_group() as tg:\n\n            async def worker() -> None:\n                async with queue.receive() as msg_handle_rcv_stream:\n                    # receive a single job\n                    async with (await msg_handle_rcv_stream.receive()).acquire():\n                        print("received")\n                        # do some work\n                        await anyio.sleep(1)\n                        print("done processing")\n                        print("acked")\n\n            tg.start_soon(worker)\n            tg.start_soon(worker)\n\n            async with queue.send(b\'{"foo":"bar"}\') as completion_handle:\n                print("sent")\n                await completion_handle.wait()\n                print("completed")\n                tg.cancel_scope.cancel()\n\n\nif __name__ == "__main__":\n    anyio.run(main)\n    # prints:\n    # "sent"\n    # "received"\n    # "done processing"\n    # "acked"\n    # "completed"\n```\n\n## Development\n\n1. Clone the repo\n2. Start a disposable PostgreSQL instance (e.g `docker run -it -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres`)\n3. Run `make test`\n\n[asyncpg]: https://github.com/MagicStack/asyncpg\n\nSee this release on GitHub: [v0.10.0](https://github.com/adriangb/pgjobq/releases/tag/0.10.0)\n',
    'author': 'Adrian Garcia Badaracco',
    'author_email': 'dev@adriangb.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/adriangb/pgjobq',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
