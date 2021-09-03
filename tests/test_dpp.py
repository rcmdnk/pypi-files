import os
import pytest
from pypi_files import __version__
from pypi_files.core import PyPiFiles

@pytest.fixture(scope='module')
def pf():
    my_pf = PyPiFiles(package='tsd2gspread', version='0.1.1',
                      file='./tests/packages.yml')
    return my_pf

def test_version():
    assert __version__ == '0.1.0'

def test_get_json(pf):
    assert pf.get_json('tsd2gspread')['info']['author'] == 'rcmdnk'

def test_get_version(pf):
    assert pf.get_version('tsd2gspread', '0.1.1') == '0.1.1'
    latest = pf.get_version('tsd2gspread', 'latest')
    assert latest != 'latest' and latest != '0.1.1'

def test_get_file(pf):
    assert pf.get_file('tsd2gspread', '0.1.1') == 'https://files.pythonhosted.org/packages/54/ab/229e1e8c00332d0be9f5ebd6c44564caef2c63c0ae06732cb2c8b9665df2/tsd2gspread-0.1.1.tar.gz'

def test_get_file_list(pf):
    files = sorted(pf.get_file_list())
    checks = sorted([
      'https://files.pythonhosted.org/packages/0b/a7/e724c8df240687b5fd62d8c71f1a6709d455c4c09432c7412e3e64f4cbe5/numpy-1.21.1.zip',
        'https://files.pythonhosted.org/packages/54/ab/229e1e8c00332d0be9f5ebd6c44564caef2c63c0ae06732cb2c8b9665df2/tsd2gspread-0.1.1.tar.gz',
      'https://files.pythonhosted.org/packages/66/03/818876390c7ff4484d5a05398a618cfdaf0a2b9abb3a7c7ccd59fe181008/numpy-1.21.0.zip',
      'https://files.pythonhosted.org/packages/cf/f7/6c0dd488b5f5f1c0c1a48637df45046334d0be684faaf3536429f14aa9de/pandas-1.3.2.tar.gz',])
    assert files == checks

def test_download(pf):
    pf.packages = {('tsd2gspread', '0.1.1')}
    pf.download()
    assert os.path.exists('./tsd2gspread-0.1.1.tar.gz')
    os.remove('./tsd2gspread-0.1.1.tar.gz')
