"""Unit tests for conda qualify"""

import pathlib

import pytest

from conda_flow import commands, shell

TEST_ROOT = pathlib.Path(__file__).parent
TEST_CONFIG_ROOT = TEST_ROOT / 'configs'
TEST_CFG_1 = TEST_CONFIG_ROOT / 'relative_example.yml'


class TestParse:
	"""Group for testing parse"""

	@pytest.mark.parametrize('cmd,cfg,name,plat,op,run,verbose', [
		('lock', '/path/to/config', 'sample-name', None, None, None, False),
		('lock', '/path/to/config', 'sample-name', 'sample-plat', None, None, False),
		('lock', '/path/to/config', 'sample-name', None, 'sample-op-env', None, False),
		('lock', '/path/to/config', 'sample-name', None, None, 'run after', False),
		('lock', '/path/to/config', 'sample-name', None, None, None, True),
	])
	def test_parse_args(self, cmd, cfg, name, plat, op, run, verbose):
		"""Test parse args"""

		args = [
			cmd,
			'-c', cfg,
			'-n', name,
		]

		if plat is not None:
			args.extend([
				'-p', plat,
			])

		if op is not None:
			args.extend([
				'--op-env', op,
			])

		if run is not None:
			args.extend([
				'--run-after', run,
			])

		if verbose:
			args.append('--verbose')

		args = commands.parse_args(args)
		assert args.command == cmd
		assert args.config == cfg
		assert args.name == name

		if plat is None:
			assert args.platform == [commands.CONDA_LOCK_PLATFORM_LINUX, commands.CONDA_LOCK_PLATFORM_MAC]
		else:
			assert args.platform == [plat]

		assert args.op_env == commands.DEFAULT_OP_ENV if op is None else op
		assert args.run_after == run
		assert args.verbose == verbose


class TestLock:
	"""Group for testing shell utils"""

	def test_lock(self):
		args = [
			'lock',
			'-c', TEST_CFG_1.as_posix(),
			'-n', 'test1',
			'-p', 'osx-64'
		]
		commands.main(args)

	@pytest.mark.skipif(not shell.is_osx(), reason='Osx only test')
	def test_activate_osx(self):
		args = [
			'activate',
			'-c', TEST_CFG_1.as_posix(),
			'-n', 'test2',
			'-p', 'osx-64'
		]
		commands.main(args)

	@pytest.mark.skipif(not shell.is_linux(), reason='Linux only test')
	def test_activate_linux(self):
		args = [
			'activate',
			'-c', TEST_CFG_1.as_posix(),
			'-n', 'test2',
			'-p', 'linux-64'
		]
		commands.main(args)


class TestInstallationChecks:

	def test_check_command_available(self):
		"""Test check command installed"""
		assert commands.check_command_available('cat', op_env=None)
		assert not commands.check_command_available('abc123cba321', op_env=None)
