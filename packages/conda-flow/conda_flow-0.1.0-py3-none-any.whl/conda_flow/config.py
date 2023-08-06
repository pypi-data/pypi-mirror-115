"""Configuration parsing and specification for conda-qualify

"""
from typing import Union

import cerberus
import pathlib
import yaml

KEY_PATHS = 'paths'
KEY_ENV_DIR = 'env_dir'
KEY_BASE_SUBPATH = 'base_subpath'
KEY_LOCK_SUBPATH = 'lock_subpath'
KEY_CREATE_IF_NOT_EXISTS = 'create_if_not_exists'
KEY_ENV_FILE_NAME_TEMPLATE = 'template'

PLACEHOLDER_KIND = 'kind'
PLACEHOLDER_NAME = 'name'
PLACEHOLDER_PLATFORM = 'platform'
FILE_NAME_TEMPLATE_PLACEHOLDERS = [PLACEHOLDER_NAME, PLACEHOLDER_PLATFORM, PLACEHOLDER_KIND]

DEFAULT_ENV_DIR = './.envs'
DEFAULT_BASE_SUBPATH = 'base'
DEFAULT_LOCK_SUBPATH = 'lock'
DEFAULT_CREATE_IF_NOT_EXISTS = False
DEFAULT_ENV_FILE_NAME_TEMPLATE = '{name}-{platform}.{kind}'

KIND_BASE = 'yml'
KIND_LOCK = 'lock'

PACKAGE_PATH = pathlib.Path(__file__).parent
DEFAULT_LOCK_PATH = PACKAGE_PATH / 'locks' / 'op-env-{platform}.lock'

# Define schema for configuration files, which will be used
# For validation with cerberus
CONDA_QUALIFY_SCHEMA = {
	KEY_PATHS: {
		'type': 'dict',
		'schema': {
			KEY_ENV_DIR: {
				'type': 'string',
				'path_exists': True,
				'default': DEFAULT_ENV_DIR,
			},
			KEY_BASE_SUBPATH: {
				'type': 'string',
				'default': DEFAULT_BASE_SUBPATH,
			},
			KEY_LOCK_SUBPATH: {
				'type': 'string',
				'default': DEFAULT_LOCK_SUBPATH,
			},
			KEY_CREATE_IF_NOT_EXISTS: {
				'type': 'boolean',
				'default': DEFAULT_CREATE_IF_NOT_EXISTS,
			},
			KEY_ENV_FILE_NAME_TEMPLATE: {
				'type': 'string',
				'file_name_template': True,
				'default': DEFAULT_ENV_FILE_NAME_TEMPLATE,
			},
		}
	},
}


class ConfigError(ValueError):
	"""Error class for configuration"""


class QualifyValidator(cerberus.Validator):
	"""Custom validator class to implement bespoke validation methods
	"""

	def _validate_path_exists(self, constraint, field, value):
		"""Validate that a path exists"""
		path = pathlib.Path(value)
		if constraint is True and path.is_absolute() and not path.exists():
			self._error(field, "Specified path must exist.")

	def _validate_file_name_template(self, constraint, field, value):
		if constraint is True:
			for p in FILE_NAME_TEMPLATE_PLACEHOLDERS:
				if '{' + p + '}' not in value:
					self._error(field, "File name template must contain {{{}}} placeholder.".format(p))


class Config:
	def __init__(self, env_dir: pathlib.Path, base_subpath: str = DEFAULT_BASE_SUBPATH, lock_subpath: str = DEFAULT_LOCK_SUBPATH,
				 create_if_not_exists: bool = False, file_name_template: str = DEFAULT_ENV_FILE_NAME_TEMPLATE):
		self.env_dir = env_dir
		self.base_subpath = base_subpath
		self.lock_subpath = lock_subpath
		self.base_subdir = self.env_dir / self.base_subpath
		self.lock_subdir = self.env_dir / self.lock_subpath
		self.create_if_not_exists = create_if_not_exists
		self.file_name_template = file_name_template
		self._kind_to_subpath = {
			KIND_BASE: self.base_subpath,
			KIND_LOCK: self.lock_subpath,
		}

	@staticmethod
	def from_dict(d: dict):
		return Config(env_dir=pathlib.Path(d[KEY_PATHS][KEY_ENV_DIR]),
					  base_subpath=d[KEY_PATHS][KEY_BASE_SUBPATH],
					  lock_subpath=d[KEY_PATHS][KEY_LOCK_SUBPATH],
					  create_if_not_exists=d[KEY_PATHS][KEY_CREATE_IF_NOT_EXISTS],
					  file_name_template=d[KEY_PATHS][KEY_ENV_FILE_NAME_TEMPLATE])

	def env_base_path(self, name: str, platform: str):
		return self.env_kind_path(name, platform, kind=KIND_BASE)

	def env_lock_path(self, name: str, platform=None):
		return self.env_kind_path(name, platform=platform, kind=KIND_LOCK)

	def env_kind_path(self, name: str, platform: str, kind: str):
		return self.env_dir / self._kind_to_subpath[kind] / self.file_name_template.format(**{
			PLACEHOLDER_NAME: name,
			PLACEHOLDER_PLATFORM: platform if platform is not None else '{{{}}}'.format(PLACEHOLDER_PLATFORM),
			PLACEHOLDER_KIND: kind,
		})


def load_config(path: Union[str, pathlib.Path], coerce: bool = True) -> Config:
	"""Utility for loading and validating a qualify config

	Args:
		path:
			str or Path, the full path to the config file

	Returns:
		dict, the config as a dictionary
	"""
	if not isinstance(path, pathlib.Path):
		path = pathlib.Path(path)

	if not path.exists():
		raise ValueError('Config file does not exist: {}'.format(path.as_posix()))

	# Read
	with open(path.as_posix(), 'r') as fid:
		try:
			cfg = yaml.load(fid)
		except Exception as e:
			raise ValueError('Problem loading config file: {}'.format(path.as_posix())) from e

	v = QualifyValidator(CONDA_QUALIFY_SCHEMA)

	# Validate
	valid = v.validate(cfg)
	if not valid:
		err_msg = '\n'.join(['Parameter {}: {}'.format(k, ','.join(v)) for k, v in sorted(v.errors.items(), key=lambda p: p[0])])
		raise ConfigError('Invalid config, see errors below:\n{}'.format(err_msg)) from e

	# Normalize
	cfg = v.normalized(cfg)

	# Make env_dir absolute, if relative make relative to config file directory
	env_dir_path = pathlib.Path(cfg[KEY_PATHS][KEY_ENV_DIR])
	if not env_dir_path.is_absolute():
		abs_env_dir = (path.parent / env_dir_path).resolve()
		cfg[KEY_PATHS][KEY_ENV_DIR] = abs_env_dir.as_posix()

	if coerce:
		return Config.from_dict(cfg)
	return cfg


DEFAULT_OP_ENV = 'conda-qualify-op-env'
