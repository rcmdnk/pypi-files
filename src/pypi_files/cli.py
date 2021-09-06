import sys
import fire
import yaml
from .core import PyPIFiles


class CliObject:
    def __init__(self, package=None, version=None, file=None, destination=None):
        self.package = package.split(',') if package is not None else None
        self.version = version.split(',') if version is not None else None
        self.file = file
        self.destination = destination

    def help(self):
        PyPIFiles().help()

    def get_file_list(self):
        files = PyPIFiles(package=self.package, version=self.version,
                          file=self.file).get_file_list()
        for f in files:
            print(f)

    def download(self):
        PyPIFiles(package=self.package, version=self.version, file=self.file,
             destination=self.destination).download()


def cli():
    if len(sys.argv) <=1 or sys.argv[1] in ["-h", "--help"]:
        PyPIFiles().help()
    else:
        fire.Fire(CliObject)
