# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['git_fzf',
 'git_fzf.commands',
 'git_fzf.lib',
 'git_fzf.lib.templates',
 'git_fzf.lib.utils']

package_data = \
{'': ['*']}

install_requires = \
['pyfzf==0.2.2']

entry_points = \
{'console_scripts': ['git-iadd = git_fzf.commands.add:run',
                     'git-icommit = git_fzf.commands.commit:run',
                     'git-idiff = git_fzf.commands.diff:run',
                     'git-idifftool = git_fzf.commands.difftool:run',
                     'git-ireset = git_fzf.commands.reset:run',
                     'git-irestore = git_fzf.commands.restore:run',
                     'git-iswitch = git_fzf.commands.switch:run']}

setup_kwargs = {
    'name': 'git-fzf',
    'version': '0.0.2',
    'description': 'Interactive versions of built-in Git commands using fzf',
    'long_description': '# git-fzf\n\ngit-fzf provides interactive versions of built-in Git commands using\n[fzf](https://github.com/junegunn/fzf).\n\nhttps://user-images.githubusercontent.com/933396/130337334-345c5c60-4e20-4807-8ed3-655bf5115981.mp4\n\n## Installation\n\nRun `pip install git-fzf`\n\n## Usage\n\n<dl>\n  <dt>\n    git iadd\n  </dt>\n  <dd>\n    Interactively choose one or more files to add\n  </dd>\n\n  <dt>\n    git icommit\n  </dt>\n  <dd>\n    Interactively choose one or more staged or unstaged files to commit\n  </dd>\n\n  <dt>\n    git idiff\n  </dt>\n  <dd>\n    Interactively choose one or more files to diff. Provide the\n    <code>--staged</code> or <code>--cached</code> flag to choose from staged\n    files.\n  </dd>\n\n  <dt>\n    git idifftool\n  </dt>\n  <dd>\n    Interactively choose one or more files to diff with the difftool. Provide\n    the <code>--staged</code> or <code>--cached</code> flag to choose from\n    staged files.\n  </dd>\n\n  <dt>\n    git ireset\n  </dt>\n  <dd>\n    Interactively choose one or more files to reset\n  </dd>\n\n  <dt>\n    git irestore\n  </dt>\n  <dd>\n    Interactively choose one or more files to restore\n  </dd>\n\n  <dt>\n    git iswitch\n  </dt>\n  <dd>\n    Interactively choose a branch to switch to. Provide the <code>-r</code> or\n    <code>--remotes</code> flag to choose from remote branches.\n  </dd>\n</dl>\n\n## Similar projects\n\nThere are some similar projects with more elaborate user interfaces:\n\n* [forgit](https://github.com/bigH/git-fuzzy)\n* [git-fuzzy](https://github.com/bigH/git-fuzzy)\n\nMost of the time, I personally prefer the more minimal user interface that this\nproject provides. Still, would I have started this project if I had known about\nthese alternatives at the time?\n\n🤷\u200d♂️\n',
    'author': 'John Karahalis',
    'author_email': 'john.karahalis@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/openjck/git-fzf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
