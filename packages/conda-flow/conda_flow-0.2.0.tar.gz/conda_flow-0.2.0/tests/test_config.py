"""Unit tests for the config module

"""

import copy
import pathlib
import tempfile

import pytest
import yaml
from conda_flow import config

CONFIG_TEMPLATE = {
	config.KEY_PATHS: {
		config.KEY_ENV_DIR: None,
		config.KEY_BASE_SUBPATH: None,
		config.KEY_LOCK_SUBPATH: None,
		config.KEY_CREATE_IF_NOT_EXISTS: None,
	}
}


def remove_none_values(d: dict):
	new_d = {}
	for k, v in d.items():
		if isinstance(v, dict):
			new_d[k] = remove_none_values(v)
		else:
			if v is not None:
				new_d[k] = v
	return new_d


class TestConfigSpec:
	"""Test group for config spec"""

	@pytest.mark.parametrize('env_dir,base_subpath,lock_subpath,create_if_not_exists,create_in_advance,err_msg,exp_vals', [
		(None, None, None, None, False, None, (config.DEFAULT_ENV_DIR, config.DEFAULT_BASE_SUBPATH, config.DEFAULT_LOCK_SUBPATH, config.DEFAULT_CREATE_IF_NOT_EXISTS)), # Check default behavior
	])
	def test_load_config(self, env_dir, base_subpath, lock_subpath, create_if_not_exists, create_in_advance, err_msg, exp_vals):
		with tempfile.TemporaryDirectory() as tmp:
			tmp_dir = pathlib.Path(tmp)
			cfg_path = tmp_dir / 'cfg.yml'

			# Assemble config
			cfg = copy.deepcopy(CONFIG_TEMPLATE)
			cfg[config.KEY_PATHS][config.KEY_ENV_DIR] = env_dir
			cfg[config.KEY_PATHS][config.KEY_BASE_SUBPATH] = base_subpath
			cfg[config.KEY_PATHS][config.KEY_LOCK_SUBPATH] = lock_subpath
			cfg[config.KEY_PATHS][config.KEY_CREATE_IF_NOT_EXISTS] = create_if_not_exists

			# Clean cfg dict
			cfg = remove_none_values(cfg)

			if create_in_advance:
				env_path = pathlib.Path(env_dir)
				if not env_path.is_absolute():
					env_path = (cfg_path / env_path).resolve()
					base_path = env_path / base_subpath
					lock_path = env_path / lock_subpath

				for p in (env_path, base_path, lock_path):
					if not p.exists():
						p.mkdir()

			# Write yaml in tmp dir
			with open(cfg_path.as_posix(), 'w') as fid:
				yaml.dump(cfg, fid)

			# Load config
			if err_msg:
				with pytest.raises(ValueError) as info:
					loaded = config.load_config(cfg_path.as_posix())

					assert str(info.value) == err_msg
			else:
				loaded = config.load_config(cfg_path.as_posix(), coerce=False)

				# unpack expected vals
				exp_env_dir, exp_base, exp_lock, exp_create = exp_vals

				# fix relative paths
				exp_env_path = pathlib.Path(exp_env_dir)
				if not exp_env_path.is_absolute():
					exp_env_path = (cfg_path.parent / exp_env_dir).resolve()

				# Test values
				assert loaded[config.KEY_PATHS][config.KEY_ENV_DIR] == exp_env_path.as_posix()
				assert loaded[config.KEY_PATHS][config.KEY_BASE_SUBPATH] == exp_base
				assert loaded[config.KEY_PATHS][config.KEY_LOCK_SUBPATH] == exp_lock
				assert loaded[config.KEY_PATHS][config.KEY_CREATE_IF_NOT_EXISTS] == exp_create
