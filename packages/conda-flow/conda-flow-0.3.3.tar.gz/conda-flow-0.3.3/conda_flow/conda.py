"""Wrappers around conda shell scripts

TODO maybe replace this with conda python api (if stable, didn't used to be)
"""
import hashlib
import pathlib
from typing import List, Tuple

from conda_flow import shell
from conda_flow.config import DEFAULT_OP_ENV


def create(name: str, lock_path: pathlib.Path, force: bool = False):
	args = [
		'create',
		'-n', name,
		'--file', lock_path.as_posix()
	]

	if force:
		args.append('--force')
	shell.run_command('conda', args)


def env_list() -> list:
	res = shell.run_command('conda', ['env', 'list'])
	clean = []
	for line in res:
		if line and not line.startswith('#') and ' ' in line:
			clean.append(line.split(' ')[0])
	return clean


def create_lock(base_path: pathlib.Path, lock_path: pathlib.Path, platform: str, op_env: str = DEFAULT_OP_ENV):
	shell.run_command('conda-lock', [
		'-f', base_path.as_posix(),
		'--filename-template', lock_path.as_posix(),
		'-p', platform,
	], conda_env=op_env)


def list_(name: str, explicit: bool = False, md5: bool = False, out_path: pathlib.Path = None):
	args = [
		'list',
		'--name', name,
	]

	if explicit:
		args.append('--explicit')

	if md5:
		args.append('--md5')

	if out_path:
		args.append('>{}'.format(out_path.as_posix()))

	shell.run_command('conda', args)


def load_lock(lock_path: pathlib.Path) -> str:
	with open(lock_path.as_posix(), 'r') as fid:
		lines = fid.readlines()

	clean = [line.strip() for line in lines if (line.strip() and not (line.startswith('#') or line.startswith('@')))]
	clean = [line.decode('utf-8') if isinstance(line, bytes) else line for line in clean]
	return ''.join(clean)


def lock_hash(lock_path: pathlib.Path) -> str:
	lock_str = load_lock(lock_path)
	return hashlib.sha256(lock_str.encode('utf-8')).hexdigest()


def init(shell_name: str = 'bash'):
	shell.run_command('conda', ['init', shell_name])


def activate(name: str, run: str = None):
	args = [
		'activate', name
	]

	shell.run_command('conda', args, run_after=run, source_profile=True)


def deactivate(name: str):
	args = [
		'deactivate'
	]

	shell.run_command('conda', args, source_profile=True)


def is_shell_initialized(shell_name: str):
	defined_envs = env_list()
	name = defined_envs[0]  # assume we can activate first env

	try:
		activate(name)
		deactivate(name)
	except shell.ShellError as e:
		if 'shell has not been properly configured' in e.args[0]:
			return False
		raise e
	return True
