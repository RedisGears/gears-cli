# GearsCli
Simple cli that allows the send python code the RedisGears

## Install
```python
pip install git+https://github.com/RedisGears/GearsCli.git
```

## Usage
```
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
