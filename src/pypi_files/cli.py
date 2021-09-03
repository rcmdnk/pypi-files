import sys
import fire
import yaml
from .core import PyPiFiles


class CliObject:
    def __init__(self, package=None, version=None, file=None, destination=None):
        self.package = package
        self.version = version
        self.file = file
        self.destination = destination

    def help(self):
        PyPiFiles().help()

    def get_file_list(self):
        files = PyPiFiles(package=self.package, version=self.version,
                          file=self.file).get_file_list()
        for f in files:
            print(f)

    def download(self):
        PyPiFiles(package=self.package, version=self.version, file=self.file,
             destination=self.destination).download()


def cli():
    if len(sys.argv) <=1 or sys.argv[1] in ["-h", "--help"]:
        PyPiFiles().help()
    else:
        fire.Fire(CliObject)
