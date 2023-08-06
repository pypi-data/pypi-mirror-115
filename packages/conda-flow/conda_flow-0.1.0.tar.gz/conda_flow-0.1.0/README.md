# conda-flow

Conda flow is a lightweight library that uses both conda and conda-lock to create, curate, and activate locked conda
environments.

## Why?

Managing changes to environment files can be challenging, especially when trying to coordinate with locked environment
details. The qualification pattern provides a simple workflow in which:

1. *base* (or unspecified) env files are edited by developers
1. *locked* (or fully specified) env files are produced by conda-lock when running conda-flow

The above workflow has the numerous advantages:

* Env changes are version-controlled
* No lock files are edited directly

In addition to the locking workflow (which is little more than a wrapper around conda-lock and some file
management), conda-flow also provides an activation workflow. When running the conda-flow activate workflow, the
following will occur:

1. Search for a lock file matching the desired env name (according to config / file structure)
1. Check if an env exists with that name:
    1. If yes, then compare checksums of envs to ensure up-to-date with lock file (removing if not)
    1. If no, create env from lock file
1. Activate desired env
1. Run additional configuration scripts as specified in config

## Installation

Not built as package yet, ultimately will be able to:

```bash
pip install conda-flow
```

```bash
conda install -c conda-forge conda-flow
```

## Usage

Create a directory in your repo for managing base and qualified env files (default is `<project_root>/.envs`). This
directory will be configurable (more docs on config options coming)

Create a base env file, with an OS specified according to the filename template (also configurable), for example
`<project_root>/.envs/base-linux-64.yml` with a minimal set of packages and specifications for your project. To generate
the qualified env `<project_root>/.envs/locks/base-linux-64.lock` (again name / location configurable), run:

```bash
conda-flow lock -n base -p linux-64
```

To activate the qualified environment, run:

```bash
conda-flow activate -n base
```

This will:

* find the proper lock file for the current OS according to the config
* check to make sure any existing defined environments with matching names have matching specifications (checksums)
* activate the environment
* run any additional configuration scripts specified

