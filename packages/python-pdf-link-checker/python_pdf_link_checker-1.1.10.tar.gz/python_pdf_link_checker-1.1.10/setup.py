# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pdf_link_checker']

package_data = \
{'': ['*']}

install_requires = \
['PyPDF2>=1.26.0,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'tqdm>=4.64.1,<5.0.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['pdf-link-checker = pdf_link_checker.main:app']}

setup_kwargs = {
    'name': 'python-pdf-link-checker',
    'version': '1.1.10',
    'description': '',
    'long_description': '# PDF Link Checker\n\n*This is a fork of the [pdf-link-checker](https://github.com/mattbriggs/pdf-link-checker).*\n\nSituation: You need to upload a PDF somewhere\n\n-  a submission to [EasyChair](https://easychair.org/cfp/)\n- a preprint to [arxiv](https://arxiv.org/)\n- a slide deck to [moodle](https://www.moodle.tum.de/)\n\nNow, you want to check if all the links are still active and that the reviewers, reader, or students end up with `404` error codes.\nLet this script check that for you!\n\n## Setup\n\n1. Install [Python](https://www.python.org/downloads/)\n2. Install the `python-pdf-link-checker` via the Python Package Registry.\n\n    ```bash\n    pip install python-pdf-link-checker\n    ```\n\n    **Attention**: On macOS, `pip` is usually the installer of the Python2 instance.\n    Please use `pip3` or `pip3.x` in this case.\n\n3. Now you should be able to call `pdf-link-checker` within your shell.\n\n    ```bash\n    $ pdf-link-checker --version\n    pdf-link-checker 1.1.5\n    ```\n\n## Usage\n\n### Check Links\n\n```bash\n$ pdf-link-checker check-links --help\nUsage: pdf-link-checker check-links [OPTIONS] [PDF_FILE]\n\n  - Get input PDF and output CSV location. - execute\n  check_pdf_links(infilepath, infilepath) - Save the report to output CSV\n  location.\n\nArguments:\n  [PDF_FILE]  The PDF file to check.\n\nOptions:\n  -r, --report FILE          The CSV file with all the checked links.\n                             [default: report.csv]\n\n  -I, --ignore-url TEXT      URL that should not be checked, e.g., because we\n                             now that they are not activated yet.  [default: ]\n\n  -C, --ci                   If set, the command will exit with an error code\n                             if there are broken URLs.  [default: False]\n\n  -c, --csv-delimiter TEXT   The CSV delimiter, e.g., `;`  [default: ;]\n  -A, --ignore-unauthorized  If this flag is set, we will ignore 403 status\n                             codes. Some websites block scripts, and thus\n                             existing links will result in 403 codes.\n                             [default: False]\n\n  --help                     Show this message and exit.\n```\n\n### Check Page Limit\n\n```bash\n$ pdf-link-checker check-page-limit --help\nUsage: pdf-link-checker check-page-limit [OPTIONS] [PDF_FILE]\n\n  Check the page limit.\n\nArguments:\n  [PDF_FILE]  The PDF file to check.\n\nOptions:\n  -l, --page-limit INTEGER  The maximal number of pages\n  --help                    Show this message and exit.\n```\n\n#### Example\n\n```bash\n$ pdf-link-checker check-links main.pdf\nStarting\n100%|█████████| 5/5 [00:30<00:00,  6.18s/it]\nDone: .../report.csv\n```\n\n## Run Pytest to validate returns\n\nFrom the script directory, run `pytest` to validate the code. The tests use the PDFs in the **data** folder.\n\n## Contact\n\nIf you have any question, please contact [Patrick Stöckle](mailto:patrick.stoeckle@tum.de?subject=GitLab%3A%20PDF-Link-Checker&body=Hi%2C%0AI%20have%20the%20following%20question%20regarding%20the%20pdf-link-checker%20library%3A).\n',
    'author': 'Matt Briggs',
    'author_email': 'mabrigg@microsoft.com',
    'maintainer': 'Patrick Stöckle',
    'maintainer_email': 'patrick.stoeckle@posteo.de',
    'url': 'https://github.com/pstoeckle/pdf-link-checker',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
