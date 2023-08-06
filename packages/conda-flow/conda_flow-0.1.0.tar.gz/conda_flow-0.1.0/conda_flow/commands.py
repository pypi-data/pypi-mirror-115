"""Primary interface for conda qualification scheme

"""
import argparse
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

	parser.add_argument('-p', '--platform', required=True, nargs='+', default=[CONDA_LOCK_PLATFORM_LINUX, CONDA_LOCK_PLATFORM_MAC],
						help="Types of platforms to be locked, can be specified multiple times.")

	parser.add_argument('--op-env', type=str, required=False, default=DEFAULT_OP_ENV,
						help="Name of operational environment (used to produce locks). Must have conda-lock installed.")

	parser.add_argument('--run-after', type=str, required=False, default=None,
						help='Command to run after environment is activated.')

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


def qualify_env(cfg: config.Config, name: str, platform: str, op_env: str = DEFAULT_OP_ENV):
	assert_conda_installed()
	assert_conda_shell_initialized()
	assert_conda_lock_installed()

	base_path = cfg.env_base_path(name, platform)
	lock_path = cfg.env_lock_path(name)
	conda.create_lock(base_path, lock_path, platform, op_env=op_env)


def activate_env(cfg: config.Config, name: str, run_after: str = None):
	if not check_command_available('conda'):
		raise ValueError('Conda must be installed. Please install miniconda.')

	required_lock_path = cfg.env_lock_path(name, platform=CONDA_LOCK_PLATFORM_MAP[shell.PLATFORM])

	if name in conda.env_list():
		# env exists, need to check hashes for equivalence
		with tempfile.TemporaryDirectory() as tmp:
			tmp_path = pathlib.Path(tmp)
			existing_lock_path = tmp_path / 'existing.lock'

			# Write out a lock file of existing env
			conda.list_(name, explicit=True, md5=True, out_path=existing_lock_path)

			existing_sha = conda.lock_hash(existing_lock_path)
			required_sha = conda.lock_hash(required_lock_path)

			if not existing_sha == required_sha:
				# SHA mismatch - need to remove and create
				conda.create(name, required_lock_path, force=True)
	else:
		conda.create(name, required_lock_path)

	# Activate env
	conda.activate(name, run=run_after)


def main(args: list = None):
	args = parse_args(args)

	# Load config
	cfg = config.load_config(args.config)

	# Establish operating environment
	if args.op_env not in conda.env_list():
		if args.op_env == DEFAULT_OP_ENV:
			conda.create(name=DEFAULT_OP_ENV, lock_path=DEFAULT_OP_ENV_LOCK)
		else:
			raise ValueError('Operational env not created')

	# Create envs directories if they do not exist
	if cfg.create_if_not_exists:
		for p in (cfg.env_dir, cfg.base_subdir, cfg.lock_subdir):
			if not p.exists():
				p.mkdir(parents=True, exist_ok=True)

	# Run the command given
	if args.command == COMMAND_LOCK:
		for platform in args.platform:
			qualify_env(cfg, args.name, platform, op_env=args.op_env)
	elif args.command == COMMAND_ACTIVATE:
		activate_env(cfg, args.name, args.run_after)
	else:
		raise ValueError('Unknown command: {}'.format(args.command))
