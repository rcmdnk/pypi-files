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
                    if p in self.packages:
                        self.packages[p].append(v)
                    else:
                        self.packages[p] = [v]

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
''')

    def get_json(self, package, version, force=False):
        if (force or self.json['package'] != package
                or self.json['version'] != version
                or self.json['json'] is None):
            if version == 'latest':
                url = f'{self.base_url}/{package}/json'
            else:
                url = f'{self.base_url}/{package}/{version}/json'
            self.json = {'package': package, 'version': version,
                         'json':requests.get(url).json()}
        return self.json['json']

    def get_version(self, package, version):
        if version != 'latest':
            return version
        return self.get_json(package, version)['info']['version']

    def get_file(self, package, version):
        v = self.get_version(package, version)
        for info in self.get_json(package, version)['releases'][v]:
            if info['packagetype'] == 'sdist':
                return info['url']
        return None

    def get_dependencies(self, package, version):
        requires_dist = self.get_json(
            package, version)['info']['requires_dist']
        print(requires_dist)
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
                    print(p, v)
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

        print(self.packages)
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
