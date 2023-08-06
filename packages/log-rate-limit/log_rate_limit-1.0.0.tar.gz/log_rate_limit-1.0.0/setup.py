# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['log_rate_limit']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'log-rate-limit',
    'version': '1.0.0',
    'description': '',
    'long_description': '# log-rate-limit - limit excessive log output\n\n[![Build Status](https://github.com/samuller/log-rate-limit/actions/workflows/tests.yml/badge.svg)](https://github.com/samuller/log-rate-limit/actions/workflows/tests.yml)\n[![Code Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](https://github.com/samuller/pgmerge/actions)\n[![Checked with mypy](https://img.shields.io/badge/mypy-strict-blue)](http://mypy-lang.org/)\n[![Formatted with black](https://img.shields.io/badge/code%20style-black-black)](https://black.readthedocs.io/en/stable/)\n\nA logging filter that can be used with Python\'s standard logging mechanism to rate-limit logs - i.e. suppress logs when they are being output too fast.\n\nLog commands are grouped into separate **streams** that will each have their own rate limitation applied without affecting the logs in other streams. By default every log is assigned a unique stream so that only "repeated" logs will be suppressed - in this case "repeated" logs doesn\'t mean identical log messages, but rather logs output from the same line of code. However, logs can also be assigned streams manually to achieve various outcomes:\n- A dynamic stream id based on the message content can be used so that different messages from the same log command can also be rate-limited separately.\n- A log can be assigned to an undefined/`None` stream so that rate-limiting doesn\'t apply to it.\n- Logs in different parts of the code can be grouped into the same stream so that they share a rate-limit, e.g. when they all trigger due to the same issue and only some are needed to indicate it.\n\n## Usage\n\n### Rate-limiting by default\n\nExample of rate-limiting with default options where each log is assigned to it\'s own stream:\n```python\nimport time\nimport logging\nfrom log_rate_limit import StreamRateLimitFilter, RateLimit\n# Setup logging\nlogging.basicConfig()\nlogger = logging.getLogger(__name__)\n\n# Add our filter\nlogger.addFilter(StreamRateLimitFilter(period_sec=1))\n# Log many warnings\nfor _ in range(100):\n    logger.warning("Wolf!")\nfor i in range(100):\n    logger.warning("No really, a wolf!")\n    if i == 98:\n        time.sleep(1)\n# Override stream as undefined to prevent rate-limiting\nfor _ in range(3):\n    logger.warning("Sheep!", extra=RateLimit(stream_id=None))\n``` \nWhich only outputs the following:\n```log\nWARNING:__main__:Wolf!\nWARNING:__main__:No really, a wolf!\nWARNING:__main__:No really, a wolf!\n+ skipped 98 logs due to rate-limiting\nWARNING:__main__:Sheep!\nWARNING:__main__:Sheep!\nWARNING:__main__:Sheep!\n```\nNote that (unless overridden) logs were only repeated after the `sleep()` call, and the repeated log also included an extra summary message added afterwards.\n\nWhen we override rate-limiting above, you\'ll see our filter reads dynamic configs from logging\'s `extra` parameter.\n\n> Be very careful not to forget the `extra=` name part of the argument, as then the logging framework will assume you\'re passing arguments meant for formatting in the logging message and your options will silently be ignored!\n\n### Rate-limit only when specified\n\nIf you want most of your logs to be unaffected and you only have some you want to specifically rate-limit, then you can do the following:\n```python\nimport logging\nfrom log_rate_limit import StreamRateLimitFilter, RateLimit\n# Setup logging\nlogging.basicConfig(level=logging.INFO)\nlogger = logging.getLogger(__name__)\n\n# Add our filter, but don\'t assign unique streams to logs by default\nlogger.addFilter(StreamRateLimitFilter(period_sec=1, all_unique=False))\n# Normal logs are now not rate-limited\nfor i in range(3):\n    logger.info(f"Status update: {i}")\n# Only those we manually assign a stream will be rate-limited\nfor _ in range(3):\n    logger.warning("Issue!", extra=RateLimit(stream_id="issue"))\n```\nWhich only outputs the following:\n```log\nINFO:__main__:Status update: 0\nINFO:__main__:Status update: 1\nINFO:__main__:Status update: 2\nWARNING:__main__:Issue!\n```\n',
    'author': 'Simon Muller',
    'author_email': 'samullers@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/samuller/log-rate-limit',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
