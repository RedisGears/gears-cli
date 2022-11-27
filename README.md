[![license](https://img.shields.io/github/license/RedisGears/gears-cli.svg)](https://github.com/RedisGears/gears-cli)
[![PyPI version](https://badge.fury.io/py/gears-cli.svg)](https://badge.fury.io/py/gears-cli)
[![CircleCI](https://circleci.com/gh/RedisGears/gears-cli/tree/master.svg?style=svg)](https://circleci.com/gh/RedisGears/gears-cli/tree/master)
[![Releases](https://img.shields.io/github/release/RedisGears/gears-cli.svg)](https://github.com/RedisGears/gears-cli/releases/latest)
 [![Known Vulnerabilities](https://snyk.io/test/github/RedisGears/gears-cli/badge.svg?targetFile=requirements.txt)](https://snyk.io/test/github/RedisGears/gears-cli?targetFile=requirements.txt)

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
Usage: gears-cli [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  export-requirements   Export requirements from RedisGears
  import-requirements   Import requirements to RedisGears
  install-requirements  Install give requirements
  run                   Run gears function


> gears-cli run --help
Usage: gears-cli run [OPTIONS] FILEPATH [EXTRA_ARGS]...

  Run gears function

Options:
  --host TEXT               Redis host to connect to
  --port INTEGER            Redis port to connect to
  --user TEXT               Redis acl user
  --password TEXT           Redis password
  --ssl BOOLEAN             Use ssl
  --ssl-password TEXT       Passphrase for ssl key
  --ssl-keyfile TEXT        Path to ssl key file
  --ssl-certfile TEXT       Path to ssl certificate file
  --ssl-ca-certs TEXT       Path to ssl ca certificate file
  --ssl-verify-ca BOOLEAN   Whether or not to us CA to verify certs
  --requirements TEXT       Path to requirements.txt file
  --help                    Show this message and exit.

> gears-cli export-requirements --help
Usage: gears-cli export-requirements [OPTIONS]

  Export requirements from RedisGears

Options:
  --host TEXT             Redis host to connect to
  --port INTEGER          Redis port to connect to
  --user TEXT             Redis acl user
  --password TEXT         Redis password
  --ssl BOOLEAN           Use ssl
  --ssl-password TEXT     Passphrase for ssl key
  --ssl-keyfile TEXT      Path to ssl key file
  --ssl-certfile TEXT     Path to ssl certificate file
  --ssl-ca-certs TEXT     Path to ssl ca certificate file
  --ssl-verify-ca BOOLEAN Whether or not to us CA to verify certs
  --save-directory TEXT   Directory for exported files
  --output-prefix TEXT    Prefix for the requirement zip file
  --registration-id TEXT  Regisrations ids to extract their requirements
  --requirement TEXT      Requirement to export
  --all                   Export all requirements
  --help                  Show this message and exit.

> gears-cli import-requirements --help
Usage: gears-cli import-requirements [OPTIONS] [REQUIREMENTS]...

  Import requirements to RedisGears

Options:
  --host TEXT               Redis host to connect to
  --port INTEGER            Redis port to connect to
  --user TEXT               Redis acl user
  --password TEXT           Redis password
  --ssl BOOLEAN             Use ssl
  --ssl-password TEXT       Passphrase for ssl key
  --ssl-keyfile TEXT        Path to ssl key file
  --ssl-certfile TEXT       Path to ssl certificate file
  --ssl-ca-certs TEXT       Path to ssl ca certificate file
  --ssl-verify-ca BOOLEAN   Whether or not to us CA to verify certs
  --requirements-path TEXT  Path of requirements directory containing
                            requirements zip files, could also be a zip file
                            contains more requirements zip files
  --all                     Import all requirements in zip file
  --bulk-size INTEGER       Max bulk size to send to redis in MB
  --help                    Show this message and exit.

> gears-cli install-requirements --help
Usage: gears-cli install-requirements [OPTIONS] [REQUIREMENTS]...

  Install give requirements

Options:
  --host TEXT               Redis host to connect to
  --port INTEGER            Redis port to connect to
  --user TEXT               Redis acl user
  --password TEXT           Redis password
  --ssl BOOLEAN             Use ssl
  --ssl-password TEXT       Passphrase for ssl key
  --ssl-keyfile TEXT        Path to ssl key file
  --ssl-certfile TEXT       Path to ssl certificate file
  --ssl-ca-certs TEXT       Path to ssl ca certificate file
  --ssl-verify-ca BOOLEAN   Whether or not to us CA to verify certs
  --requirements-file TEXT  Path to requirements.txt file
  --help                    Show this message and exit.
```
