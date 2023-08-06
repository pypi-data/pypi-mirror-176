# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['devpair']
install_requires = \
['GitPython>=3.1.29,<4.0.0',
 'click>=8.1.3,<9.0.0',
 'loguru>=0.6.0,<0.7.0',
 'nox>=2022.8.7,<2023.0.0']

setup_kwargs = {
    'name': 'devpair',
    'version': '1.1.1',
    'description': 'Pair script that manage a pair programming session using git.',
    'long_description': '<div align="center">\n    <img src="./logo.png" width="60px">\n</div>\n\n## Dev Pair\n\n[![Python Test](https://github.com/raphaelkieling/pair/actions/workflows/push.yml/badge.svg)](https://github.com/raphaelkieling/pair/actions/workflows/push.yml)\n\nIt\'s a tool to facilitate the pair programming session. Instead of make a lot of `git add, git commit, git push, git pull`, you can make it more quickly only running `devpair start, devpair next`.\n\nVery useful for teams that like to make pair sessions often. If you neve was a driver or a navigator feel free to read [here](https://martinfowler.com/articles/on-pair-programming.html) to have a context.\n\n## Install\n\n```\npip install devpair\n```\n\n## How it works?\n\nYou will work inside a temporary pair branch that in the end all the commits will be squashed to be added to the feature branch.\n\n<details>\n    <summary>Under the hood</summary>\n  \nUnder the hood the `devpair start` will take your current branch and create a copy with the same name but with the prefix `pair` \n\nAfter make your code changes the `devpair next` will add, commit and push your code using an internal commit message. This step will be more easier to understand checking the [example step by step](#example-of-use)\n\nIn the end, we have the `devpair done` that will add, commit, push and delete the branch. Don\'t worry we will make a squash commit of everything that you did for the current branch.\n\n</details>\n\n[![](https://mermaid.ink/img/pako:eNqNkMEKwjAMhl9l5Dzx3rPgA3jtJbb_1uLajpgiMvbu1oOgDGE5fSTfn0AWcsWDDI1Rz8JzsLlr5UpKUbd8Fc4udBmPwwDWKtjlzxzluDv0wwHuVqpuTybIiH-bP6nEMX_rG5N6apOm-faD5d2zpAEJlkxDj4HrpJZsXpvKVcvlmR0ZlYqe6uxZcYo8CicyA093rC_K-3GZ?type=png)](https://mermaid.live/edit#pako:eNqNkMEKwjAMhl9l5Dzx3rPgA3jtJbb_1uLajpgiMvbu1oOgDGE5fSTfn0AWcsWDDI1Rz8JzsLlr5UpKUbd8Fc4udBmPwwDWKtjlzxzluDv0wwHuVqpuTybIiH-bP6nEMX_rG5N6apOm-faD5d2zpAEJlkxDj4HrpJZsXpvKVcvlmR0ZlYqe6uxZcYo8CicyA093rC_K-3GZ)\n\n### Example of use\n\n```bash\n# Dev A\nmain $ devpair start\npair/main $ echo "hello" > welcome.txt\npair/main $ devpair next\n\n# Dev B\nmain $ devpair start\npair/main $ cat welcome.txt # shows "hello"\npair/main $ echo " world" >> welcome.txt\npair/main $ devpair next\n\n# Dev A again\npair/main $ devpair start\npair/main $ cat welcome.txt # shows "hello world"\npair/main $ echo "!" >> welcome.txt\npair/main $ devpair done\n\nmain $ git commit -m "feat: created hello world feature"\nmain $ git push\n\n# Dev B again\npair/main $ devpair done # just to clear the house. \n\n\n# Any Dev\npair/main $ devpair summary # print a summary\n\nLast Dev: \n     dev-a@gmail.com  | 2022-11-16 00:40:00\nFirst Dev: \n     dev-a@gmail.com  | 2022-11-15 17:55:19\nFrequence: \n     dev-a@gmail.com         | ▇▇ 2\n     dev-b@gmail.com         | ▇ 1\n```\n\nif you have any doubt\n\n```\ndevpair --help\n```\n\n### Recommendations\n\n- Before the pair programming\n    - Define the end of the session. How many time do you want pair?\n    - Define the break time.\n- Use a `timer` like. Ordered by preference, for some cases a mobile timer is enough.\n    - https://cuckoo.team/\n    - https://double-trouble.wielo.co/\n    - http://mobtimer.zoeetrope.com/\n- The `driver` need to share the screen avoiding to use tools like `vscode live share`, even they are good it can create some hard moments that you want to show the browser or create a quickly diagram. The preference is that the `driver` ever need to share the screen.\n- Antipatterns: https://tuple.app/pair-programming-guide/antipatterns\n\n\n### Contributing\n\nFork, create a branch from `main` with the pattern `feat/my-feature` and make a pull request with your proposal.\n\n### Local env\n\n```sh\n# Set the version\npyenv local 3.10.4\n# Run all the tests\npython -m pytest\n\n# Set the develop\nmake local-env\n# Run the devpair\npython -m localdevpair ...\n```\n\n### Publishing\n\n```sh\n# it\'s using twine $HOME/.pypirc [testpypi]\nmake publish-test\n\n# it\'s using twine $HOME/.pypirc [pypi]\nmake publish\n```\n',
    'author': 'raphael.kieling',
    'author_email': 'raphael.kieling@telus.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
