import os
from . import file_utils


_templates_dir = os.path.join(os.path.dirname(__file__), 'templates')


def gen_cpp_project(path):
    template = os.path.join(_templates_dir, 'cpp', 'project')

    os.mkdir(path)
    name = os.path.basename(path)
    file_utils.copy(template, path, {'project': name})


def gen_cpp_module(path):
    template = os.path.join(_templates_dir, 'cpp', 'module')

    dirname, name = os.path.split(path)
    file_utils.copy(template, dirname, {'module': name})


def gen_py_project(path):
    raise NotImplementedError('gen_py_module')


def gen_py_script(path):
    template = os.path.join(_templates_dir, 'py', 'script')

    dirname, name = os.path.split(path)
    file_utils.copy(template, dirname, {'script': name})
