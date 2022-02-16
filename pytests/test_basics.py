from gears_cli import run, install_requirements, export_requirements, import_requirements
from click.testing import CliRunner
from RLTest import Defaults
import os

Defaults.decode_responses = True

def set_acl_user(env):
    env.expect('ACL', 'SETUSER', 'foo', 'on', '>pass', '+@all').ok()

def run_internal_test(env, extra_args=[]):
    runner = CliRunner()
    result = runner.invoke(run, extra_args + ['./pytests/example.py'])
    env.assertEqual(result.exit_code, 0)
    env.assertContains('"1"', result.output)

def requirements_internal_test(env, extra_args=[], after_restart_callback=None):
    runner = CliRunner()
    result = runner.invoke(install_requirements, extra_args + ['redis'])
    env.assertEqual(result.exit_code, 0)
    env.assertContains('Done', result.output)

    # export requirement redis
    result = runner.invoke(export_requirements, extra_args + ['--requirement', 'redis'])
    env.assertEqual(result.exit_code, 0)
    env.assertContains('Saving exported requirement into', result.output)

    env.stop()
    env.start()
    if after_restart_callback:
        after_restart_callback(env)

    # import redis requirement
    result = runner.invoke(import_requirements, extra_args + ['--requirements-path', './', 'redisgears-requirement-v1-redis-linux-focal-x64.zip'])
    env.assertEqual(result.exit_code, 0)
    env.assertContains('imported successfully', result.output)

    os.remove('./redisgears-requirement-v1-redis-linux-focal-x64.zip')

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
