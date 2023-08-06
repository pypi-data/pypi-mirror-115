"""Primary interface for conda flow scheme

"""
import argparse
import logging
import pathlib
import sys
import tempfile

from conda_flow import config, conda, shell
from conda_flow.config import DEFAULT_OP_ENV
from conda_flow.shell import run_command, SHELL_COMMAND_WHICH, CONDA_LOCK_PLATFORM_LINUX, CONDA_LOCK_PLATFORM_MAC, CONDA_LOCK_PLATFORM_MAP, \
	DEFAULT_OP_ENV_LOCK

COMMAND_LOCK = 'lock'
COMMAND_ACTIVATE = 'activate'


def parse_args(args: list = None):
	"""Parse command line arguments using argparse

	Args:
		args:
			List[str] list of arguments to parse. Default None. If None, use system command line input.

	Returns:
		Namespace, the parsed arguments
	"""
	# Default behavior is command line arguments
	if args is None:
		args = sys.argv[1:]

	parser = argparse.ArgumentParser()
	parser.add_argument('command', type=str, choices=[COMMAND_LOCK, COMMAND_ACTIVATE],
						help='Command, either {} or {}'.format(COMMAND_ACTIVATE, COMMAND_LOCK))

	parser.add_argument('-c', '--config', type=str, required=True,
						help="Full path to config file.")

	parser.add_argument('-n', '--name', required=True,
						help="Name of environment to qualify or activate")

	parser.add_argument('-p', '--platform', required=False, nargs='+', default=[CONDA_LOCK_PLATFORM_LINUX, CONDA_LOCK_PLATFORM_MAC],
						help="Types of platforms to be locked, can be specified multiple times.")

	parser.add_argument('--op-env', type=str, required=False, default=DEFAULT_OP_ENV,
						help="Name of operational environment (used to produce locks). Must have conda-lock installed.")

	parser.add_argument('--run-after', type=str, required=False, default=None,
						help='Command to run after environment is activated.')

	parser.add_argument('--verbose', required=False, action='store_true',
						help='If specified, set logging level to debug.')

	return parser.parse_args(args)


def check_command_available(command: str, op_env: str = DEFAULT_OP_ENV):
	"""Check command installed"""
	res = run_command(SHELL_COMMAND_WHICH, [command], conda_env=op_env, source_profile=True)
	return bool(res)


def assert_conda_installed():
	if not check_command_available('conda', op_env=None):
		raise ValueError('Conda must be installed. Please install miniconda.')


def assert_conda_shell_initialized():
	if not conda.is_shell_initialized('bash'):
		raise ValueError('Conda bash shell must be initialized, please do so by running `conda init bash`')


def assert_conda_lock_installed(op_env=DEFAULT_OP_ENV):
	if not check_command_available('conda-lock', op_env=op_env):
		raise ValueError('Conda-lock must be installed. Please install conda-lock into the op environment.')


def lock_env(cfg: config.Config, name: str, platform: str, op_env: str = DEFAULT_OP_ENV):
	"""Create an env lock file

	Args:
		cfg:
			Config, the configuration object
		name:
			str, the name of the env to activate
		platform:
			str, the type of platform to lock
		op_env:
			str, default 'conda-flow-op-env', the operational env

	Returns:
		None
	"""
	assert_conda_installed()
	assert_conda_shell_initialized()
	assert_conda_lock_installed()

	base_path = cfg.env_base_path(name, platform)
	lock_path = cfg.env_lock_path(name)
	conda.create_lock(base_path, lock_path, platform, op_env=op_env)


def activate_env(cfg: config.Config, name: str, run_after: str = None):
	"""Activate an env

	Args:
		cfg:
			Config, the configuration object
		name:
			str, the name of the env to activate
		run_after:
			str, default None, if specified run this command after env activation

	Returns:
		None
	"""
	assert_conda_installed()
	assert_conda_shell_initialized()

	required_lock_path = cfg.env_lock_path(name, platform=CONDA_LOCK_PLATFORM_MAP[shell.PLATFORM])

	if name in conda.env_list():
		# env exists, need to check hashes for equivalence

		logging.debug('Env {} already defined, checking for consistency with lock'.format(name))
		with tempfile.TemporaryDirectory() as tmp:
			tmp_path = pathlib.Path(tmp)
			existing_lock_path = tmp_path / 'existing.lock'

			# Write out a lock file of existing env
			conda.list_(name, explicit=True, md5=True, out_path=existing_lock_path)

			existing_sha = conda.lock_hash(existing_lock_path)
			required_sha = conda.lock_hash(required_lock_path)

			if not existing_sha == required_sha:
				# SHA mismatch - need to remove and create
				logging.debug('Existing env {} mismatch with lock, recreating.'.format(name))
				conda.create(name, required_lock_path, force=True)
	else:
		logging.debug('Env {} not defined, creating from lock.'.format(name))
		conda.create(name, required_lock_path)

	# Activate env
	logging.debug('Activating env {}'.format(name))
	conda.activate(name, run=run_after)


def main(args: list = None):
	args = parse_args(args)

	# Setup Logging
	logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.DEBUG if args.verbose else logging.INFO)
	logging.debug(
		'Running conda-flow with args:\n\t{}'.format('\n\t'.join('{}: {}'.format(n, v) for n, v in zip(['command', 'config', 'name', 'platform', 'op_env', 'run_after', 'verbose'],
																									 [args.command, args.config, args.name, args.platform, args.op_env, args.run_after,
																									  args.verbose]))))

	# Load config
	logging.debug('Loading config file from: {}'.format(args.config))
	cfg = config.load_config(args.config)

	# Establish operating environment
	logging.debug('Checking for operating environment: {}'.format(args.op_env))
	if args.op_env not in conda.env_list():
		logging.debug('Operating env not yet created.')
		if args.op_env == DEFAULT_OP_ENV:
			logging.debug('Creating default operating env.')
			conda.create(name=DEFAULT_OP_ENV, lock_path=DEFAULT_OP_ENV_LOCK)
		else:
			raise ValueError('Operational env not created')

	# Create envs directories if they do not exist
	logging.debug('Checking if env directories exist.')
	if cfg.create_if_not_exists:
		for p in (cfg.env_dir, cfg.base_subdir, cfg.lock_subdir):
			if not p.exists():
				logging.debug('Creating missing env dir: {}'.format(p.as_posix()))
				p.mkdir(parents=True, exist_ok=True)

	# Run the command given
	logging.debug('Running given command')
	if args.command == COMMAND_LOCK:
		for platform in args.platform:
			logging.debug('Creating lock for {} on platform {}'.format(args.name, platform))
			lock_env(cfg, args.name, platform, op_env=args.op_env)
	elif args.command == COMMAND_ACTIVATE:
		logging.debug('Activating env {} with run after: {}'.format(args.name, args.run_after))
		activate_env(cfg, args.name, args.run_after)
	else:
		raise ValueError('Unknown command: {}'.format(args.command))
