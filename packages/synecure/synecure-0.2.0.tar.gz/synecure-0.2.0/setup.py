# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['synecure']

package_data = \
{'': ['*']}

install_requires = \
['coleo>=0.2.1,<0.3.0']

entry_points = \
{'console_scripts': ['sy = synecure.cli:entry_sy',
                     'sy-bsync = synecure.cli:entry_bsync',
                     'sy-config = synecure.cli:entry_sy_config']}

setup_kwargs = {
    'name': 'synecure',
    'version': '0.2.0',
    'description': 'File sync utility',
    'long_description': '\n# Synecure\n\nSynecure provides a command line program called `sy` that allows easy synchronization of files and directories over SSH between different machines. It is mostly a wrapper around [bsync](https://github.com/dooblem/bsync), which is itself based on the standard UNIX tool `rsync`.\n\nThis is beta software and comes with **NO GUARANTEES** that it will keep your data safe. It should not be used as backup solution.\n\n\n## Install\n\n```bash\npip install synecure\n```\n\n\n## Usage\n\n```bash\n# Sync local ~/directory with remote $HOME/directory on me@awesome.person\nsy ~/directory -r me@awesome.person\n\n# Sync current directory with the same path on me@awesome.person, port 2222\nsy -r me@awesome.person -p 2222\n\n# Synchronize to a named remote from your SSH config\nsy -r me\n\n# Synchronize the current directory to the last used remote (for that directory)\nsy\n```\n\nBy default, `sy` can take on any path within your `$HOME` and will set the corresponding path on the remote\'s `$HOME`. It is possible to change this behavior or synchronize paths outside of `$HOME` using the `sy-config add-path` command.\n\n`sy` with no argument will sync the current directory using the last remote for that directory (you will need to use the -r flag the first time, but not subsequently).\n\n\n## Howto\n\n\n### Ignore files\n\nAdd a `.bsync-ignore` file in the root directory to sync with a filename or glob pattern on each line, and they will be ignored. It works more or less like `.gitignore`.\n\nPutting `.bsync-ignore` files in subdirectories to ignore files in these subdirectories will unfortunately not work, so `sy ~/x` and `sy ~/x/y` may synchronize the contents of `~/x/y` differently if both directories contain different `.bsync-ignore` files, or if one has an ignore file and the other does not.\n\n\n### Global ignores\n\nThe `sy-config ignore` command can be used to generally ignore files or directories:\n\n```bash\n# Edit the ignore file using $EDITOR, if it is set\nsy-config ignore\n\n# List all existing ignores\nsy-config ignore -l\n\n# Ignore all files that end with ~\n# Do not forget the single quotes here, to avoid shell expansion!\nsy-config ignore \'*~\'\n\n# Unignore files that end with ~\nsy-config ignore -r \'*~\'\n```\n\nThe ignores work mostly like `.gitignore` or `.bsync-ignore` above, but they apply globally. Note that `sy` will also read *remote-side* global ignores when syncing to a remote. Global ignores are located at `$HOME/.config/synecure/ignore`, so a remote can define some global ignores even without installing `sy` remote-side. Global ignores local-side, remote-side, as well as `.bsync-ignore` files local-side and remote-side are all merged together.\n\n\n### Customize synchronization paths\n\nTo synchronize local `/etc` to remote `/etcetera`, for named remote `desktop`:\n\n```bash\nsy-config add-path desktop /etc /etcetera\n```\n\nObviously, this will only work if the remote user has the permissions to write to `/etcetera`. You can have multiple remotes for the same host with different users, if that helps.\n\nTo synchronize local `~/hello` to remote `~/bonjour`:\n\n```bash\nsy-config add-path desktop ~/hello bonjour\n```\n\nDon\'t use `~` for the remote path, it will complete to the wrong thing.\n\nTo list available remotes and paths:\n\n```bash\nsy-config list\n```\n\n### Sync local directories\n\n```bash\nsy-config add dropbox file://~/Dropbox\n```\n\n## Other options\n\n### Dry run\n\nUse the `-n` flag to perform a "dry run": `sy` (well, `bsync`) will report all the transfers that would occur but it will not perform them.\n\nUse `--show-plan` to get the sequence of commands that `sy` will run.\n\n### Conflict resolution\n\nWhenever a file was modified on both ends since the last sync, `sy` will ask which one you want to keep.\n\nUse `sy <options> --resolve local` (or `sy <options> -1`) to always keep the local file without prompting, or `--resolve remote` (or `-2`) to always keep the remote file.\n\n### List directories\n\n`sy -l` will list all directories that have been previously synced using the tool, along with the last remote they were synced to (remember that `sy` without the `-r` option will sync to the last remote).\n\n## Configuration files\n\n* `~/.config/synecure/remotes.json` defines protocols and paths for named remotes.\n  * You can open an editor for that file with `sy-config edit`\n* `~/.config/synecure/ignore` lists global ignores.\n  * You can open an editor for that file with `sy-config ignore`\n* `~/.config/synecure/directories.json` maps directories to last used remotes.\n* `~/.ssh/config` is the standard location to define host information for `ssh`.\n  * For convenience, you can open an editor for that file with `sy-config ssh`\n',
    'author': 'Olivier Breuleux',
    'author_email': 'breuleux@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/breuleux/synecure',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
