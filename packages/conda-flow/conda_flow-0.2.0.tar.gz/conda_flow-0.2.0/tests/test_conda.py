"""Unit tests for conda qualify"""

import conda_flow.conda
import conda_flow.shell
from conda_flow import commands


class TestCondaAPIUtilities:
	"""Group for testing conda api utils"""

	def test_conda_env_list(self):
		"""Test conda env list"""
		res = conda_flow.conda.env_list()
		assert isinstance(res, list)
