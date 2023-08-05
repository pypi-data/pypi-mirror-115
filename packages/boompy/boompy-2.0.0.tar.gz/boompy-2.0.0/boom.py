"""
A simple text-based key-value store for your command line.
"""
import os
import pathlib
import sys
import argparse
import platform
import subprocess


__author__ = 'Bill Israel <bill.israel@hey.com>'
__version__ =  '.'.join(map(str, (2, 0, 0)))


XDG_CONFIG_HOME = os.environ.get('XDG_CONFIG_HOME', pathlib.Path('~/.config/').expanduser())
BOOMDIR = XDG_CONFIG_HOME / 'boom'
DEFAULT_DB = BOOMDIR / 'boomdb'


class Boom:
    def __init__(self, filepath):
        self.db = {}
        self.filepath = pathlib.Path(filepath).expanduser()

        self.filepath.parent.mkdir(exist_ok=True)
        self.filepath.touch(exist_ok=True)

        with open(self.filepath, 'r') as f:
            for line in f:
                key, value = line.strip().split('\t', maxsplit=1)
                self.db[key] = value

    def save(self):
        with open(self.filepath, 'w') as f:
            f.writelines(f'{key}\t{value}\n' for key, value in self.items())

    def __getitem__(self, key):
        return self.db[key]

    def __setitem__(self, key, value):
        self.db[key] = value

    def __contains__(self, key):
        return key in self.db

    def __delitem__(self, key):
        del self.db[key]

    def __len__(self):
        return len(self.db)

    def __iter__(self):
        return iter(self.db)

    def items(self):
        return self.db.items()

    def get(self, key, default=None):
        return self.db.get(key, default)

    def keys(self):
        return self.db.keys()

    def clear(self):
        self.db.clear()


def parse_args():
    parser = argparse.ArgumentParser(description='Simple command line snippets')
    parser.add_argument('--version', action='version',
                        version='%(prog)s {} by {}'.format(__version__, __author__))
    parser.add_argument('key', type=str, nargs='?', help='The key to retrieve the value for')
    parser.add_argument('value', type=str, nargs='?', help='The value to set for the key')
    parser.add_argument('--database', '-db', dest='database', default=DEFAULT_DB,
                        help='File path where the boom database is located')
    parser.add_argument('--overwrite', '-o', action='store_true', default=False,
                        help='Overwrite any existing value for the given key')
    parser.add_argument('--delete', '-d', action='store_true', default=False,
                        help='Delete the given key')
    return parser.parse_args()


def copy_to_clipboard(value):
    """Copy a string value to the system clipboard."""
    COPY_COMMAND = {
        'Darwin': ['pbcopy'],
        'Windows': ['clip'],
        'Linux': ['xclip', '-selection', 'clipboard']
    }
    cmd = COPY_COMMAND[platform.system()]
    pipe = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    pipe.communicate(value)
    return not bool(pipe.returncode)


def main():
    """
    Get, set, or delete a key. Boom.
    """
    args = parse_args()

    get_key = bool(args.key and not (args.value or args.delete))
    add_key = bool(args.key and args.value and not args.overwrite)
    delete_key = bool(args.key and not args.value and args.delete)
    update_key = bool(args.key and args.value and args.overwrite)

    try:
        snippets = Boom(args.database)

        if get_key:
            if args.key in snippets:
                if copy_to_clipboard(snippets.get(args.key).encode('utf-8')):
                    print(f"'{args.key}' successfully copied to clipboard.")
            else:
                print(f"'{args.key}' not found in database.", file=sys.stderr)
        elif add_key:
            if args.key in snippets:
                raise ValueError(f'Key {args.key} already exists, use --overwrite to force save.')

            snippets[args.key] = args.value
            print(f"'{args.key}' is now '{args.value}'.")
        elif delete_key:
            del snippets[args.key]
            print(f"'{args.key}' has been removed.")
        elif update_key:
            snippets[args.key] = args.value
            print(f"'{args.key}' is now '{args.value}'.")
        else:
            if snippets:
                max_key_length = max(map(len, snippets.keys()))
                for key, value in snippets.items():
                    print(f'{key:<{max_key_length}}\t{value}')

        snippets.save()
        return 0
    except Exception as ex:
        print(f'Error: {ex}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())

