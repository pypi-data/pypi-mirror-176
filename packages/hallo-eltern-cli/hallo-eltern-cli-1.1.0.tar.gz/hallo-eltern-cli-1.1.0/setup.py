# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hallo_eltern_cli', 'hallo_eltern_cli.commands']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.17.0,<3.0.0']

entry_points = \
{'console_scripts': ['hallo-eltern-cli = hallo_eltern_cli.cli:run']}

setup_kwargs = {
    'name': 'hallo-eltern-cli',
    'version': '1.1.0',
    'description': "Command-line/Python/Email interface for 'Hallo!Eltern' app for Upper-Austrian schools",
    'long_description': '# hallo-eltern-cli\n\n[![Tests](https://github.com/somechris/hallo-eltern-cli/workflows/Tests/badge.svg)](https://github.com/somechris/hallo-eltern-cli/actions?query=workflow%3ATests)\n\n`hallo-eltern-cli` is a command-line/Python/email interface for\n[Education Group GmbH](https://www.edugroup.at/)\'s\n"[Hallo!Eltern](https://hallo-eltern.klassenpinnwand.at/)" application\nfor Upper-Austrian schools.\n\n`hallo-eltern-cli` is not affiliated with Education Group GmbH or their\n"Hallo!Eltern" application in any way. The "Hallo!Eltern" application is a\nproduct of the Education Group GmbH.\n\n`hallo-eltern-cli` allows to list, messages, read them, download\nattachments, etc directly from your Linux terminal and allows to get\nfull messages including attachments directly to your local inbox.\n\n## Table of Contents\n\n1. [Installation](#installation)\n1. [CLI Commands](#cli-commands)\n1. [Email Integration](#email-integration)\n    1. [Email server (SMTP)](#email-server-smtp)\n    1. [Mail Delivery Agent (MDA)](#mail-delivery-agent-mda)\n\n## Installation\n\nYou need Python `>=3.7`\n\n1. Install the package:\n\n   ```\n   pip3 install hallo-eltern-cli\n   ```\n\n1. Set the credentials from your "Hallo!Eltern" application:\n\n    ```\n    hallo-eltern-cli config --email YOUR-EMAIL@EXAMPLE.ORG --password YOUR-PASSWORD\n    ```\n\n1. Done \\o/\n\n`hallo-eltern-cli` is now ready for use. For example to list messages,\nuse the `list` command:\n\n```\nhallo-eltern-cli list\n[...]\n\nFlags |   Id    | Subject\n---------------------------------------------------\n CC   | 1234567 | Wandertag am Donnerstag\n CC   | 3456789 | Schikurs Anmeldung\n  C   | 2345678 | Fehlendes Arbeitsblatt\n```\n\n## CLI commands\n\nThe CLI offers the following commands:\n\n* `list` lists available messages\n* `show` shows a message\n* `open` marks a message as open\n* `close` marks a message as closed\n* `config` updates and dumps the configuration\n* `test` tests the configured user againts the API\n* `mda` feeds messages into a message delivery agend (procmail, maildrop, ...)\n* `stdout` dumps messages to stdout\n* `smtp` sends messages as emails\n* `version` prints the version number\n\n## Email integration\n\nSimple ways to integrate `hallo-eltern-cli` with your email pipelines\nare to either\n\n* [forward the messages to an email server (SMTP)](#email-server-smtp)\n    (e.g.: gmx, office365, local server), or to\n* [pipe the messages to a message delivery agent\n    (MDA)](#mail-delivery-agent-mda) (e.g.: `procmail`, `maildrop`).\n\n### Email server (SMTP)\n\nThe `smtp` mode of `hallo-eltern-cli` allows to send the messages\n(containing the full message\'s text and attachments) to an email\nserver to get them to your usual email inbox.\n\nTo run check for new messages and forward them to your inbox for\nexample 12 minutes into every hour, simply add a crontab entry like:\n\n```\n12 * * * * /path/to/hallo-eltern-cli smtp --force-address your-email-address@example.org\n```\n\nand configure the email server to use in `$HOME/.config/hallo-eltern-cli/config`\n\n* Local SMTP server\n\n    The default configuration of `hallo-eltern-cli` is to submit to a\n    local SMTP server through `localhost:25`. So you do not need to add\n    any configuration.\n\n* GMX\n\n    To submit the messages to your GMX inbox, set the `[smtp]` section\n    in your `$HOME/.config/hallo-eltern-cli/config` to:\n\n    ```\n    [smtp]\n    host = mail.gmx.net\n    port = 587\n    starttls = True\n    user = your-email-address@gmx.at\n    password = your-secret-password\n    ```\n\n    (Note that the password gets stored in plain text, so secure your\n    config file through external means)\n\n* Office365 / Hotmail\n\n    To submit the messages to your Office365 or Hotmail inbox, set the\n    `[smtp]` section in your `$HOME/.config/hallo-eltern-cli/config`\n    to:\n\n    ```\n    [smtp]\n    host = smtp.office365.com\n    port = 587\n    starttls = True\n    user = your-email-address@hotmail.com\n    password = your-secret-password\n    ```\n\n    (Note that the password gets stored in plain text, so secure your\n    config file through external means)\n\n\n### Mail Delivery Agent (MDA)\n\nThe `mda` mode of `hallo-eltern-cli` allows to format messages as\nemails (containing the full message\'s text and attachments) and submit\nthem to a mail delivery agent (MDA, e.g. `procmail`). To run it for\nexample 12 minutes into every hour, simply add a crontab entry like:\n\n```\n12 * * * * /path/to/hallo-eltern-cli mda\n```\n',
    'author': 'Christian Aistleitner',
    'author_email': 'christian@quelltextlich.at',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/somechris/hallo-eltern-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
