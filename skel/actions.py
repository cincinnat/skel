import os
from . import file_utils


_templates_dir = os.path.join(os.path.dirname(__file__), 'templates')

def _gen_project(lang, path):
    template = os.path.join(_templates_dir, lang, 'project')

    os.mkdir(path)
    name = os.path.basename(path)
    name = name.replace('-', '_')
    file_utils.copy(template, path, {'project': name})


def _simple_gen(lang, target, path):
    template = os.path.join(_templates_dir, lang, target)

    dirname, name = os.path.split(path)
    if not dirname:
        dirname = '.'
    file_utils.copy(template, dirname, {target: name})


def gen_cpp_project(path):
    _gen_project('cpp', path)


def gen_cpp_module(path):
    _simple_gen('cpp', 'module', path)


def gen_py_project(path):
    _gen_project('py', path)


def gen_py_script(path):
    if path.endswith('.py'):
        path = path[:-3]
    _simple_gen('py', 'script', path)
