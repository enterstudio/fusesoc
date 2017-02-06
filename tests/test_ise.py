import difflib
import os
import pytest
import tempfile

from fusesoc.config import Config
from fusesoc.core import Core
from fusesoc.coremanager import CoreManager
from fusesoc.main import _get_core, _import

def test_ise():
    params = '--vlogparam_bool --vlogparam_int=42 --vlogparam_str=hello'
    params += ' --vlogdefine_bool --vlogdefine_int=42 --vlogdefine_str=hello'

    tmpdir = tempfile.mkdtemp()
    Config().build_root = os.path.join(tmpdir, 'build')
    Config().cache_root = os.path.join(tmpdir, 'cache')

    cores_root = os.path.join(os.path.dirname(__file__),
                              'cores')
    CoreManager().add_cores_root(cores_root)
    core = _get_core("atlys")

    backend =_import('build', core.main.backend)(core, export=False)
    backend.configure(params.split())

    tcl_file = core.name.sanitized_name + '.tcl'
    reference_tcl = os.path.join(os.path.dirname(__file__), __name__, tcl_file)
    generated_tcl = os.path.join(backend.work_root, tcl_file)

    assert os.path.exists(generated_tcl)

    with open(reference_tcl) as f1, open(generated_tcl) as f2:
        assert not ''.join(difflib.unified_diff(f1.readlines(), f2.readlines()))
