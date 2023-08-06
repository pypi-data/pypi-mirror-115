"""Unit tests for conda qualify"""

import os
import pathlib

from conda_flow import shell


class TestShellUtilities:
	"""Group for testing shell utils"""

	def test_run_command(self):
		"""Test run command"""
		conda_prefix = os.environ.get('CONDA_PREFIX', None)
		res = shell.run_command('which', ['python'])

		if conda_prefix is not None:
			conda_path = pathlib.Path(conda_prefix)
			python_path = pathlib.Path(res[0])
			relative = python_path.relative_to(conda_path)
			assert relative.as_posix() == 'bin/python'
