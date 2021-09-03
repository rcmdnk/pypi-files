import os
import yaml
import requests


class PyPiFiles:
    def __init__(self, package=None, version=None, file=None,
                 destination=None, base_url='https://pypi.org/pypi'):
        self.packages = set()
        if package is not None:
            if type(package) in (list, tuple, set):
                version = version if type(version) in (
                    list, tuple, set) and len(package) == len(
                        version) else ['latest'] * len(package)
                self.packages |= set(zip(package, version))
            else:
                version = version if version is not None else 'latest'
                self.packages |= {(package, version)}
        if file is not None:
            with open(file) as f:
                self.packages |= set(list(x.items())[0]
                                     for x in yaml.safe_load(f))

        self.base_url = base_url.rstrip('/')
        if destination is None:
            destination = '.'
        self.set_destination(destination)
        self.json = {'package': None, 'json': None}

    def help(self):
        print('Help!')

    def get_json(self, package, force=False):
        if force or self.json['package'] != package \
                or self.json['json'] is None:
            self.json = {'package': package, 'json':requests.get(
                          f'{self.base_url}/{package}/json').json()}
        return self.json['json']

    def get_version(self, package, version):
        if version != 'latest':
            return version
        return self.get_json(package, version)['info']['version']

    def get_file(self, package, version):
        v = self.get_version(package, version)
        for info in self.get_json(package, v)['releases'][v]:
            if info['packagetype'] == 'sdist':
                return info['url']
        return None

    def get_file_list(self):
        files = []
        for p, v in self.packages:
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

        for p, v in self.packages:
            file =self.get_file(p, v)
            if file is None:
                print(f'No source file is found for {p}!')
                continue
            file_name = os.path.basename(file)
            output = f'{self.destination}/{file_name}'
            print(f'Downloading {file} to {output}...')
            data = requests.get(file).content
            with open(output, mode='wb') as f:
                f.write(data)
