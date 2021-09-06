import os
import copy
import yaml
import requests


class PyPIFiles:
    def __init__(self, package=None, version=None, file=None,
                 destination=None, dependencies=False,
                 base_url='https://pypi.org/pypi'):
        self.packages = {}
        if package is not None:
            if type(package) in (list, tuple, set):
                version = version if type(version) in (
                    list, tuple, set) and len(package) == len(
                        version) else ['latest'] * len(package)
                for p, v in zip(package, version):
                    if p in self.packages:
                        self.packages[p].append(v)
                    else:
                        self.packages[p] = [v]
            else:
                version = version if version is not None else 'latest'
                if package in self.packages:
                    self.packages[package].append(version)
                else:
                    self.packages[package] = [version]
        if file is not None:
            with open(file) as f:
                for p, v in [tuple(x.items())[0] for x in yaml.safe_load(f)]:
                    if p not in self.packages:
                        self.packages[p] = []
                    if type(v) is list:
                        self.packages[p] += v
                    else:
                        self.packages[p].append(v)

        self.base_url = base_url.rstrip('/')
        if destination is None:
            destination = '.'
        self.dependencies = dependencies
        self.set_destination(destination)
        self.json = {'package': None, 'version': None, 'json': None}

    def help(self):
        print('''Usage: pf <command> [--package <pacakge>] [--version <version>] [--file <yaml_file>] [--destination <destination>] [--base_url <base_url>] [--dependencies <bool>]

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
''')

    def parse_version(self, package, version):
        if version.startswith(package):
            if version.endswith('whl'):
                return version.replace(f'{package}-', '').split('-')[0]
            else:
                return version.replace(f'{package}-', '').replace(
                    '.tar.gz', '').replace('.zip', '')
        return version

    def get_json(self, package, version, force=False):
        if (force or self.json['package'] != package
                or self.json['version'] != version
                or self.json['json'] is None):
            if version == 'latest':
                url = f'{self.base_url}/{package}/json'
            else:
                v = self.parse_version(package, version)
                url = f'{self.base_url}/{package}/{v}/json'
            self.json = {'package': package, 'version': version,
                         'json':requests.get(url).json()}
        return self.json['json']

    def get_version(self, package, version):
        v = self.parse_version(package, version)
        if v == 'latest':
            return self.get_json(package, v)['info']['version']
        return v

    def get_file(self, package, version):
        v = self.get_version(package, version)
        sdist = None
        for info in self.get_json(package, version)['releases'][v]:
            if version.startswith(package):
                if os.path.basename(info['url']) == version:
                    return info['url']
            if info['packagetype'] == 'sdist':
                if not version.startswith(package):
                    return info['url']
                else:
                    sdist = info['url']
        return sdist

    def get_dependencies(self, package, version):
        requires_dist = self.get_json(
            package, version)['info']['requires_dist']
        if not requires_dist:
            return []
        return [x.split()[0].split('[')[0].split(';')[0].split('>')[0]
                for x in requires_dist]

    def add_dependencies(self):
        packages = copy.deepcopy(self.packages)
        while True:
            new_packages = {}
            for p in packages:
                for v in packages[p]:
                    for d in self.get_dependencies(p, v):
                        if d not in self.packages:
                            self.packages[d] = ['latest']
                            new_packages[d] = ['latest']
            if not new_packages:
                break
            packages = new_packages

    def get_file_list(self):
        if self.dependencies:
            self.add_dependencies()
        files = []
        for p in self.packages:
            for v in self.packages[p]:
                files.append(self.get_file(p, v))
        return files

    def set_destination(self, destination=None):
        if destination is None:
            destination = self.destination
        if destination is None:
            destination = '.'
        self.destination = destination.rstrip('/')

    def download(self, destination=None):
        self.set_destination(destination)

        for p in self.packages:
            for v in self.packages[p]:
                file =self.get_file(p, v)
                if file is None:
                    print(f'No source file is found for {p}-{v}!')
                    continue
                file_name = os.path.basename(file)
                output = f'{self.destination}/{file_name}'
                print(f'Downloading {file} to {output}...')
                data = requests.get(file).content
                with open(output, mode='wb') as f:
                    f.write(data)
