# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['personal_man', 'personal_man.controllers', 'personal_man.core']

package_data = \
{'': ['*']}

install_requires = \
['beartype>=0.11.0',
 'cement>=3.0.8',
 'loguru>=0.6.0',
 'pydantic>=1.9.1',
 'questionary>=1.10.0',
 'rich>=12.5.1']

entry_points = \
{'console_scripts': ['pman = personal_man:run']}

setup_kwargs = {
    'name': 'personal-man',
    'version': '1.1.0',
    'description': 'Personal Manpages (pman)',
    'long_description': '# personal-man (`pman`)\n\nPersonal Manpages\n\n## Installation\n\n1. [Install `ripgrep`](https://github.com/BurntSushi/ripgrep/tree/000015791742bb1280f1853adb714fdee1ba9f8e#installation)\n\n1. Install the `pman` CLI with pipx\n\n   ```sh\n   pipx install personal-man\n   ```\n\n1. Run `pman` to check that installation succeeded and to see the available commands\n\n1. The help output will display the directory for your personal manpages, but you can change the default by exporting an environment variable: `PMAN_DOC_PATH`. I personally have a directory within my main Obsidian vault so that I can edit the files in [Obsidian](https://obsidian.md/) and search with `pman`\n\n## Usage\n\n![VHS Demo](./demo.gif)\n\nFor more example code, see the [scripts] directory or the [tests].\n\n## Project Status\n\nSee the `Open Issues` and/or the [CODE_TAG_SUMMARY]. For release history, see the [CHANGELOG].\n\n## Contributing\n\nWe welcome pull requests! For your pull request to be accepted smoothly, we suggest that you first open a GitHub issue to discuss your idea. For resources on getting started with the code base, see the below documentation:\n\n- [DEVELOPER_GUIDE]\n- [STYLE_GUIDE]\n\n## Code of Conduct\n\nWe follow the [Contributor Covenant Code of Conduct][contributor-covenant].\n\n### Open Source Status\n\nWe try to reasonably meet most aspects of the "OpenSSF scorecard" from [Open Source Insights](https://deps.dev/pypi/personal_man)\n\n## Responsible Disclosure\n\nIf you have any security issue to report, please contact the project maintainers privately. You can reach us at [dev.act.kyle@gmail.com](mailto:dev.act.kyle@gmail.com).\n\n## License\n\n[LICENSE]\n\n[changelog]: ./docs/CHANGELOG.md\n[code_tag_summary]: ./docs/CODE_TAG_SUMMARY.md\n[contributor-covenant]: https://www.contributor-covenant.org\n[developer_guide]: ./docs/DEVELOPER_GUIDE.md\n[license]: https://github.com/kyleking/personal-man/LICENSE\n[scripts]: https://github.com/kyleking/personal-man/scripts\n[style_guide]: ./docs/STYLE_GUIDE.md\n[tests]: https://github.com/kyleking/personal-man/tests\n',
    'author': 'Kyle King',
    'author_email': 'dev.act.kyle@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyleking/personal_man',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10.5,<4.0.0',
}


setup(**setup_kwargs)
