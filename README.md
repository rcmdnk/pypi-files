# pypi-files
[![pytest](https://github.com/rcmdnk/pypi-files/actions/workflows/test.yml/badge.svg)](https://github.com/rcmdnk/pypi-files/actions/workflows/test.yml)
[![version](https://img.shields.io/pypi/v/pypi-files.svg)](https://pypi.python.org/pypi/pypi-files/)
[![license](https://img.shields.io/pypi/l/pypi-files.svg)](https://pypi.python.org/pypi/pypi-files/)

Check and download package source files from PyPI.


# Rqeuirement

* Python: tested with 3.6 or later

# Install

    $ pip install pypi-files

# Development

If you want to test/develop pypi-files, checkout the repository and use Poetry:

    $ pip install poetry # or brew install poetry
    $ git clone git@github.com/rcmdnk/pypi-files
    $ cd pypi-files
    $ poetry install
    $ poetry run pf get_file_list pypi-files
    $ # etc...

# Usage

    Usage: pf <command> [--package <pacakge>] [--version <version>] [--file <yaml_file>] [--destination <destination>] [--base_url <base_url>] [--dependencies <bool>]
    
    command:
      get_file_list    Show package source file URLs.
      download         Download package source files.
    
    Options:
      --package <package>          Set packages to check. Multiple packages can be set by separating by `,`. At least one of package or file option is needed for `get_file_list` and `download` commands.
      --version <version>          Set versions for each packages. It should be same length of `--package` input.
      --file <yaml_file>           Set YAML file which has a package list.
      --destination <destination>  Set a destination in which download files are stored. Default is `./`.
      --base_url <base_url>        Set base ufl for PyPI. Default is `httss://pypi.osg/pypi`.
      --dependencies <bool>        Set 1 to include all package dependencies.


To get package source files, use `pf get_file_list`:

    pf get_file_list [--package <pacakge>] [--version <version>] [--file <yaml file>]

You can give a package name by `--pacakge` and give a version as an option.
If `--version` is not passed, the latest version will be used.

    $ pf get_file_list --package pandas --version 1.3.2
    https://files.pythonhosted.org/packages/cf/f7/6c0dd488b5f5f1c0c1a48637df45046334d0be684faaf3536429f14aa9de/pandas-1.3.2.tar.gz


`version` can be a file name of wheel, like `pandas-1.3.2-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl`.
For this `version`, it returns path for the wheel file:

    https://files.pythonhosted.org/packages/55/51/fb64df42fd821331ab868c552452966d607eaac2c986fc3e7a50e1bf2951/pandas-1.3.2-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl

You can also use YAML file with a package list.

The file should be a list of dictionaries (`<package>: <version>`) like:

    ---
    - pandas: 1.3.2
    - numpy: latest
    - numpy: 1.21.0

If you want the latest version, use `latest`.

    $ pf get_file_list --files ./packages.yml
    https://files.pythonhosted.org/packages/cf/f7/6c0dd488b5f5f1c0c1a48637df45046334d0be684faaf3536429f14aa9de/pandas-1.3.2.tar.gz
    https://files.pythonhosted.org/packages/3a/be/650f9c091ef71cb01d735775d554e068752d3ff63d7943b26316dc401749/numpy-1.21.2.zip
    https://files.pythonhosted.org/packages/66/03/818876390c7ff4484d5a05398a618cfdaf0a2b9abb3a7c7ccd59fe181008/numpy-1.21.0.zip

To download package source files, use `download`.
You can set output destination by `--destination`.

    pf download [--package <pacakge>] [--version <version>] [--file <yaml file>] [--destination <destination>]

The default destination is current directory (`./`).

    $ pf download --package pandas --version 1.3.2
    Downloading https://files.pythonhosted.org/packages/cf/f7/6c0dd488b5f5f1c0c1a48637df45046334d0be684faaf3536429f14aa9de/pandas-1.3.2.tar.gz to ./pandas-1.3.2.tar.gz...
    $ ls
    pandas-1.3.2.tar.gz
