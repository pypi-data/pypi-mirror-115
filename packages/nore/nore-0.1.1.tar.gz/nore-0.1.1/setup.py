# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nore']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0', 'pydantic>=1.8.2,<2.0.0']

entry_points = \
{'console_scripts': ['nore = nore.main:app']}

setup_kwargs = {
    'name': 'nore',
    'version': '0.1.1',
    'description': 'Download .gitignore files from the github/gitignore repo.',
    'long_description': "# nore -- Completely Unnecessary .gitignore Management\n\n## Features\n\n* Supports 128 environments and growing\n* Optionally specify a location for the .gitignore file\n\n## Planned Features\n\n* Add support for github/gitignore/Global .gitignore templates\n* Add support for github/gitignore/community .gitignore templates\n* Option to merge .gitignore files together rather than overwrite\n* Detect and merge into a user's global .gitignore\n* Add completions\n\n## Installation\n\nInstall nore by running:\n\n```shell\npip install nore\n```\nor better yet\n\n```shell\npipx install nore\n```\n\n## Usage\n\n```\nUsage: nore [OPTIONS] [LANGUAGE]\n\nArguments:\n  [LANGUAGE]  Language for created .gitignore file.\n\nOptions:\n  -l, --list               List available .gitignore language.\n  --output-path DIRECTORY  Where to create the .gitignore file.\n\n  --install-completion     Install completion for the current shell.\n  --show-completion        Show completion for the current shell, to copy it\n                           or customize the installation.\n\n  --help                   Show this message and exit.\n```\n\nCreate a python .gitignore file in the current directory by running\n```shell\n>> nore new python\nCreated .gitignore at .\n```\n\nList all available .gitignore types by running\n```shell\n>> nore list\nactionscript              godot                     python               \nada                       gradle                    qooxdoo              \nagda                      grails                    qt                   \nandroid                   gwt                       r                    \nappceleratortitanium      haskell                   rails                \nappengine                 idris                     raku                 \narchlinuxpackages         igorpro                   rhodesrhomobile      \nautotools                 java                      ros                  \nc                         jboss                     ruby                 \nc++                       jekyll                    rust                 \ncakephp                   jenkins_home              sass                 \ncfwheels                  joomla                    scala                \nchefcookbook              julia                     scheme               \nclojure                   kicad                     scons                \ncmake                     kohana                    scrivener            \ncodeigniter               kotlin                    sdcc                 \ncommonlisp                labview                   seamgen              \ncomposer                  laravel                   sketchup             \nconcrete5                 leiningen                 smalltalk            \ncoq                       lemonstand                stella               \ncraftcms                  lilypond                  sugarcrm             \ncuda                      lithium                   swift                \nd                         lua                       symfony              \ndart                      magento                   symphonycms          \ndelphi                    maven                     terraform            \ndm                        mercury                   tex                  \ndrupal                    metaprogrammingsystem     textpattern          \neagle                     nanoc                     turbogears2          \nelisp                     nim                       twincat3             \nelixir                    node                      typo3                \nelm                       objective-c               umbraco              \nepiserver                 ocaml                     unity                \nerlang                    opa                       unrealengine         \nexpressionengine          opencart                  visualstudio         \nextjs                     oracleforms               vvvv                 \nfancy                     packer                    waf                  \nfinale                    perl                      wordpress            \nforcedotcom               phalcon                   xojo                 \nfortran                   playframework             yeoman               \nfuelphp                   plone                     yii                  \ngcov                      prestashop                zendframework        \ngitbook                   processing                zephir               \ngo                        purescript                                     \n```\n\n",
    'author': 'Trenten Oliver',
    'author_email': 'trentenoliver@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tcoliver/nore',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
