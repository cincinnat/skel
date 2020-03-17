import os
from jinja2 import Template


def get_target_fname(fname, context):
    ''' Apply template rules to a file name.
    '''

    path = fname.split('/')

    def apply_template(item):
        item = Template(item).render(context)
        if item.startswith('_') and not item.startswith('__'):
            item = '.' + item[1:]
        return item

    path = map(apply_template, path)
    return '/'.join(path)


def copy_template(source, target, context):
    ''' Apply template rules to `source` file and write to `target`.
    '''

    with open(source, 'r') as f:
        contents = f.read()
        contents = Template(contents).render(context)

    dirname = os.path.dirname(target)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    with open(target, 'w') as f:
        f.write(contents)


def list_dir(path):
    ''' Recursively list a directory.

    Return a generator producing the contents of a directory
    (relative to `path`), excluding any hidden files.
    '''

    def walk(root):
        with os.scandir(root) as it:
            for entry in it:
                if entry.name.startswith('.'):
                    continue

                fullname = os.path.join(root, entry.name)
                yield fullname
                if entry.is_dir():
                    yield from walk(fullname)

    for entry in walk(path):
        yield os.path.relpath(entry, path)


def copy(source_dir, target_dir, context):
    ''' Recursively copy a directory.

    The target directory must already exist. Do nothing and return False
    if any target file is already present in the target directory.
    '''

    if not os.path.exists(target_dir):
        raise FileNotFoundError(target_dir)
    if not os.path.isdir(target_dir):
        raise NotADirectoryError(target_dir)

    sources = list_dir(source_dir)
    sources = list(sources)

    targets = map(lambda path: get_target_fname(path, context), sources)
    targets = list(targets)

    # make sure that no target already exists
    for path in targets:
        if os.path.exists(os.path.join(target_dir, path)):
            raise FileExistsError(path)

    # apply templates and copy to the target directory
    for source, target in zip(sources, targets):
        source = os.path.join(source_dir, source)
        target = os.path.join(target_dir, target)

        if os.path.isdir(source):
            os.mkdir(target)
        else:
            copy_template(source, target, context)
