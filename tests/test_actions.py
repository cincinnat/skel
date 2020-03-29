import os
from contextlib import contextmanager

# pylint: disable=unused-wildcard-import,wildcard-import
from skel.actions import *


@contextmanager
def chdir(path):
    cur_cwd = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(cur_cwd)


def test_gen_cpp_project(tmpdir):
    path = os.path.join(tmpdir, 'proj')
    gen_cpp_project(path)

    assert os.path.exists(os.path.join(path, 'CMakeLists.txt'))


def test_gen_cpp_module(tmpdir):
    path = os.path.join(tmpdir, 'mod')
    gen_cpp_module(path)

    assert os.path.exists(path + '.cpp')
    assert os.path.exists(path + '.h')


def test_gen_py_script(tmpdir):
    path = os.path.join(tmpdir, 'script')
    gen_py_script(path)

    assert os.path.exists(path + '.py')


def test_gen_py_script_curdir(tmpdir):
    with chdir(tmpdir):
        path = 'script'
        gen_py_script(path)

        assert os.path.exists(path + '.py')


def test_gen_py_script_trailing_py(tmpdir):
    path = os.path.join(tmpdir, 'script.py')
    gen_py_script(path)

    assert os.path.exists(path)


def test_gen_py_project(tmpdir):
    path = os.path.join(tmpdir, 'proj')
    gen_py_project(path)

    assert os.path.exists(os.path.join(path, 'setup.py'))
    assert os.path.exists(os.path.join(path, 'proj'))
