# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zoom_chat_anonymizer',
 'zoom_chat_anonymizer.classes',
 'zoom_chat_anonymizer.logic']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['zoom-chat-anonymizer = zoom_chat_anonymizer.main:app']}

setup_kwargs = {
    'name': 'zoom-chat-anonymizer',
    'version': '0.1.9',
    'description': '',
    'long_description': "# Zoom Chat Anonymizer\n\n```bash\n$ zoom-chat-anonymizer --help                      \nUsage: zoom-chat-anonymizer [OPTIONS] COMMAND [ARGS]...\n\n  Helpful script to process Zoom chats.\n\nOptions:\n  --version  Version\n  --help     Show this message and exit.\n\nCommands:\n  anonymize-zoom-chats       Anonymize Zoom chats.\n  create-html-from-markdown  Create HTML files from the markdown files.\n```\n\n## Anonymize Zoom Chats\n\n```bash\n$ zoom-chat-anonymizer anonymize-zoom-chats --help\nUsage: zoom-chat-anonymizer anonymize-zoom-chats [OPTIONS] [INPUT_FOLDER]\n\n  Anonymize Zoom chats.\n\nArguments:\n  [INPUT_FOLDER]  The folder with the chat files.  [default: .]\n\nOptions:\n  -o, --output-folder DIRECTORY  The script will write the anonymized files in\n                                 this folder.  [default: out]\n  -t, --tutor TEXT               The tutors' names. The script will preserve\n                                 these names in the chat protocol.\n  -p, --pause-file FILE          A JSON file with the pauses made during the\n                                 lecture/tutorial.\n  -s, --starting-time TEXT       The starting time of the lecture/tutorial.\n                                 [default: 14:15]\n  --help                         Show this message and exit.\n```\n\n## Create HTML from Markdown\n\n```bash\n$ zoom-chat-anonymizer create-html-from-markdown --help\nUsage: zoom-chat-anonymizer create-html-from-markdown [OPTIONS]\n\n  Create HTML files from the markdown files.\n\nOptions:\n  --bib_file FILE\n  -i, --input_folder DIRECTORY\n  --help                        Show this message and exit.\n```\n",
    'author': 'Patrick Stoeckle',
    'author_email': 'patrick.stoeckle@posteo.de',
    'maintainer': 'Patrick Stöckle',
    'maintainer_email': 'patrick.stoeckle@posteo.de',
    'url': 'https://github.com/pstoeckle/Zoom-Chat-Anonymizer.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
