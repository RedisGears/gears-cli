[![license](https://img.shields.io/github/license/RedisGears/gears-cli.svg)](https://github.com/RedisGears/gears-cli)
[![PyPI version](https://badge.fury.io/py/gears-cli.svg)](https://badge.fury.io/py/gears-cli)
[![CircleCI](https://circleci.com/gh/RedisGears/gears-cli/tree/master.svg?style=svg)](https://circleci.com/gh/RedisGears/gears-cli/tree/master)
[![Releases](https://img.shields.io/github/release/RedisGears/gears-cli.svg)](https://github.com/RedisGears/gears-cli/releases/latest)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/RedisGears/gears-cli.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/RedisGears/gears-cli/context:python)

# gears-cli
Simple cli that allows the send python code to RedisGears

## Install
```python
pip install gears-cli
```

## Install latest code 

```python
pip install git+https://github.com/RedisGears/gears-cli.git
```

## Usage
```
> gears-cli --help
usage: gears-cli [-h] [--host HOST] [--port PORT]
                 [--requirements REQUIREMENTS] [--password PASSWORD]
                 path [extra_args [extra_args ...]]

Run gears scripts on Redis(Gears)

positional arguments:
  path                  scripts paths
  extra_args            extra argument to send with the script (default: [])

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           redis host (default: localhost)
  --port PORT           redis port (default: 6379)
  --requirements REQUIREMENTS
                        requirements file (default: None)
  --password PASSWORD   redis password (default: None)
```
