"""Unit tests for conda qualify"""

import pathlib

import pytest

from conda_flow import commands, shell

TEST_ROOT = pathlib.Path(__file__).parent
TEST_CONFIG_ROOT = TEST_ROOT / 'configs'
TEST_CFG_1 = TEST_CONFIG_ROOT / 'relative_example.yml'


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
