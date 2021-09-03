# pypi-files
Check and download package source files from PyPi

# Rqeuirement

* Python: tested with 3.6 or later

# Install

    $ pip install pypi-files

# Usage

To get package source files, use `pf get_file_list`:

    pf get_file_list [--package <pacakge>] [--version <version>] [--file <yaml file>]

You can give a package name by `--pacakge` and give a version as an option.
If `--version` is not passed, the latest version will be used.

    $ pf get_file_list --package pandas --version 1.3.2
    https://files.pythonhosted.org/packages/cf/f7/6c0dd488b5f5f1c0c1a48637df45046334d0be684faaf3536429f14aa9de/pandas-1.3.2.tar.gz

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

The default destination is current directory (`./`).

    $ pf download --package pandas --version 1.3.2
    Downloading https://files.pythonhosted.org/packages/cf/f7/6c0dd488b5f5f1c0c1a48637df45046334d0be684faaf3536429f14aa9de/pandas-1.3.2.tar.gz to ./pandas-1.3.2.tar.gz...
    $ ls
    pandas-1.3.2.tar.gz
