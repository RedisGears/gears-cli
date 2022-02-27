from gears_cli import run, install_requirements, export_requirements, import_requirements
from click.testing import CliRunner
from RLTest import Defaults
import os

Defaults.decode_responses = True

SSL_ARGS = ['--ssl', '--ssl-keyfile', './tests/tls/redis.key', '--ssl-certfile', './tests/tls/redis.crt', '--ssl-ca-certs', './tests/tls/ca.crt', '--ssl-password', 'foobar']

def set_acl_user(env):
    env.expect('ACL', 'SETUSER', 'foo', 'on', '>pass', '+@all').ok()

def run_internal_test(env, extra_args=[]):
    runner = CliRunner()
    result = runner.invoke(run, extra_args + SSL_ARGS + ['./pytests/example.py'])
    env.assertEqual(result.exit_code, 0)
    env.assertContains('"1"', result.output)

def requirements_internal_test(env, extra_args=[], after_restart_callback=None):
    runner = CliRunner()
    result = runner.invoke(install_requirements, extra_args + SSL_ARGS + ['redis'])
    env.assertEqual(result.exit_code, 0)
    env.assertContains('Done', result.output)

    # export requirement redis
    result = runner.invoke(export_requirements, extra_args + SSL_ARGS + ['--requirement', 'redis'])
    env.assertEqual(result.exit_code, 0)
    env.assertContains('Saving exported requirement into ', result.output)
    exported_file_path = result.output[result.output.find('/') : result.output.find('zip') + 3]

    env.stop()
    env.start()
    if after_restart_callback:
        after_restart_callback(env)

    # import redis requirement
    result = runner.invoke(import_requirements, extra_args + SSL_ARGS + ['--requirements-path', os.path.dirname(exported_file_path), os.path.basename(exported_file_path)])
    env.assertEqual(result.exit_code, 0)
    env.assertContains('imported successfully', result.output)

    os.remove(exported_file_path)

def test_run(env):
    run_internal_test(env)

def test_requirements(env):
    requirements_internal_test(env)

def test_run_acl_user_and_password(env):
    # create a new acl user
    set_acl_user(env)
    run_internal_test(env, ['--user', 'foo', '--password', 'pass'])

def test_requirements_acl_user_and_password(env):
    # create a new acl user
    set_acl_user(env)
    requirements_internal_test(env, ['--user', 'foo', '--password', 'pass'], set_acl_user)
