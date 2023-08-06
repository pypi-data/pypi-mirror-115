"""Shell utilities

"""
import pathlib
import subprocess
import sys
from typing import List

from conda_flow import config

PLATFORM_LINUX = 'linux'
PLATFORM_MAC = 'darwin'
PLATFORM_WIN = 'win32'
SHELL_COMMAND_WHICH = 'which'
CONDA_LOCK_PLATFORM_LINUX = 'linux-64'
CONDA_LOCK_PLATFORM_MAC = 'osx-64'
CONDA_LOCK_PLATFORM_MAP = {
	PLATFORM_LINUX: CONDA_LOCK_PLATFORM_LINUX,
	PLATFORM_MAC: CONDA_LOCK_PLATFORM_MAC,
}

PLATFORM = sys.platform


def is_linux():
	return PLATFORM == PLATFORM_LINUX


def is_osx():
	return PLATFORM == PLATFORM_MAC


if is_linux():
	DEFAULT_OP_ENV_LOCK = pathlib.Path(config.DEFAULT_LOCK_PATH.as_posix().format(platform=CONDA_LOCK_PLATFORM_LINUX))
	SOURCE_BASH = 'source ~/.bashrc'
elif is_osx():
	DEFAULT_OP_ENV_LOCK = pathlib.Path(config.DEFAULT_LOCK_PATH.as_posix().format(platform=CONDA_LOCK_PLATFORM_MAC))
	SOURCE_BASH = 'source ~/.bash_profile'
else:
	raise ValueError('Platform unsupported: {}'.format(PLATFORM))

STDERR_LOCKFILE_0 = 'Generating lockfile(s) for'
STDERR_LOCKFILE_1 = ' - Install lock using :'


class ShellError(ValueError):
	pass


def run_command(cmd: str, args: List[str], env: dict = None, conda_env: str = None, run_after: str = None, source_profile: bool = False):
	"""Utility for running a command in a shell with configured env"""
	resolved_cmds = [cmd + ' ' + ' '.join(args)]

	if conda_env is not None:
		if not source_profile:
			source_profile = True
		resolved_cmds = ['conda activate {}'.format(conda_env)] + resolved_cmds

	if run_after is not None:
		resolved_cmds = resolved_cmds + [run_after]

	if source_profile:
		resolved_cmds = [SOURCE_BASH] + resolved_cmds

	resolved = ' && '.join(resolved_cmds)

	p = subprocess.Popen(
		resolved,
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE,
		env=env,
		shell=True,  # TODO see if we can run multiple commands without this
		executable='/bin/bash',
	)
	stdout, stderr = list(p.stdout), list(p.stderr)
	stderr = [s.decode('utf-8') for s in stderr]

	if stderr:
		if not (stderr[0].startswith(STDERR_LOCKFILE_0) and stderr[1].startswith(STDERR_LOCKFILE_1)):
			raise ShellError('Unsuccessful command {} with args {}.\nResolved: {}\n Error message: {}'.format(cmd, args, resolved, ' '.join(stderr)))

	return [b.decode('utf-8').strip() for b in stdout]
