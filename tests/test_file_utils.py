import os
import pytest
from jinja2 import Template

# pylint: disable=unused-wildcard-import,wildcard-import
from skel.file_utils import *


def read_file(fname):
    with open(fname) as f:
        return f.read()


def write_file(fname, text):
    with open(fname, 'w') as f:
        f.write(text)


def create_dir(root, entries):
    os.makedirs(root, exist_ok=True)

    for entry in entries:
        path = os.path.join(root, entry)
        if path.endswith('/'):
            os.mkdir(path)
        else:
            with open(path, 'w'):
                pass


def test_get_target_fname():
    assert get_target_fname('foo', {}) == 'foo'
    assert get_target_fname('{{foo}}', {'foo': 'bar'}) == 'bar'
    assert get_target_fname('path/{{foo}}', {'foo': 'bar'}) == 'path/bar'

    assert get_target_fname('_foo', {}) == '.foo'
    assert get_target_fname('path/_foo', {}) == 'path/.foo'


def test_copy_template(tmpdir):
    in_file = os.path.join(tmpdir, 'in')
    out_file = os.path.join(tmpdir, 'out')

    in_text = 'some text with some {{word}}'
    context = dict(word='template')

    expected_text = Template(in_text).render(context)
    write_file(in_file, in_text)

    copy_template(in_file, out_file, context)
    out_text = read_file(out_file)

    assert out_text == expected_text


def test_list_files(tmpdir):
    sources = [
        'dir/',
        'dir/subdir/',
        'dir/subdir/sub-subdir/',
        'dir/subdir/sub-subdir/file',
        'dir/.hidden-dir/',
        'dir/.hidden-dir/file',
        'dir/file',
        'dir/.hidden-file',
    ]
    create_dir(tmpdir, sources)

    targets = list_dir(tmpdir)

    def is_not_hidden(path):
        path = path.split('/')
        hidden = filter(lambda tok: tok.startswith('.'), path)
        return next(hidden, None) is None
    expected_targets = filter(is_not_hidden, sources)
    expected_targets = map(lambda p: p.rstrip('/'), expected_targets)

    assert sorted(targets) == sorted(expected_targets)


def test_copy(tmpdir):
    sources = [
        'dir/',
        'dir/subdir/',
        'dir/subdir/sub-subdir/',
        'dir/subdir/sub-subdir/file',
        'dir/.hidden-dir/',
        'dir/.hidden-dir/file',
        'dir/file',
        'dir/.hidden-file',
    ]

    in_dir = os.path.join(tmpdir, 'in')
    create_dir(in_dir, sources)
    sources = list_dir(in_dir)

    out_dir = os.path.join(tmpdir, 'out')
    os.mkdir(out_dir)
    copy(in_dir, out_dir, {})
    targets = list_dir(out_dir)

    assert sorted(sources) == sorted(targets)


def test_copy_file_templates(tmpdir):
    in_dir = os.path.join(tmpdir, 'in')
    create_dir(in_dir, [])
    in_text = 'var = {{val}}'
    write_file(os.path.join(in_dir, 'somefile'), in_text)

    context = dict(val=42)

    out_dir = os.path.join(tmpdir, 'out')
    os.mkdir(out_dir)
    copy(in_dir, out_dir, context)
    out_text = read_file(os.path.join(out_dir, 'somefile'))

    expected_text = Template(in_text).render(context)

    assert out_text == expected_text


def test_copy_filename_templates(tmpdir):
    sources = [
        '_hidden',
        '__not_hidden',
        '{{name}}.py',
    ]
    in_dir = os.path.join(tmpdir, 'in')
    create_dir(in_dir, sources)

    context = dict(name='main')

    expected = [
        '.hidden',
        '__not_hidden',
        'main.py',
    ]

    out_dir = os.path.join(tmpdir, 'out')
    os.mkdir(out_dir)
    copy(in_dir, out_dir, context)
    targets = os.listdir(out_dir)

    assert sorted(targets) == sorted(expected)


def test_copy_when_target_exists(tmpdir):
    in_dir = os.path.join(tmpdir, 'in')
    out_dir = os.path.join(tmpdir, 'out')

    os.mkdir(in_dir)
    os.mkdir(out_dir)

    write_file(os.path.join(in_dir, 'file1'), '')
    write_file(os.path.join(in_dir, 'file2'), '')
    write_file(os.path.join(out_dir, 'file1'), '')

    with pytest.raises(FileExistsError):
        copy(in_dir, out_dir, {})
    assert not os.path.exists(os.path.join(out_dir, 'file2'))


def test_copy_missing_target_dir(tmpdir):
    in_dir = os.path.join(tmpdir, 'in')
    out_dir = os.path.join(tmpdir, 'out')

    os.mkdir(in_dir)

    with pytest.raises(FileNotFoundError):
        copy(in_dir, out_dir, {})

    write_file(out_dir, '')
    with pytest.raises(NotADirectoryError):
        copy(in_dir, out_dir, {})
