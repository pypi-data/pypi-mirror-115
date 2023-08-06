# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['exam2pptvideo',
 'exam2pptvideo._entry',
 'exam2pptvideo.de',
 'exam2pptvideo.en',
 'exam2pptvideo.es']

package_data = \
{'': ['*'],
 'exam2pptvideo.de': ['soundaffects/*', 'templates/*'],
 'exam2pptvideo.en': ['soundaffects/*', 'templates/*'],
 'exam2pptvideo.es': ['soundaffects/*', 'templates/*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'pdf2image>=1.15.1,<2.0.0',
 'python-pptx>=0.6.18,<0.7.0']

entry_points = \
{'console_scripts': ['exam_csv2pptx = exam2pptvideo._entry.command:csv2pptx',
                     'exam_pptx2media = '
                     'exam2pptvideo._entry.command:pptx2pdf2images',
                     'exam_pptx2video = '
                     'exam2pptvideo._entry.command:pptx2video',
                     'exam_pptx_validate = '
                     'exam2pptvideo._entry.validation:validate']}

setup_kwargs = {
    'name': 'exam2pptvideo',
    'version': '0.1.5',
    'description': 'Video generator for language exam',
    'long_description': '# Installation\n\n```\npip3 install --verbose exam2pptvideo \n```\n\n# Usage\n\nPlease refer to [api docs](https://qishe-ttt.github.io/exam2pptvideo/).\n\n### Execute usage\n\n* Validate ppt template\n```\nexam_pptx_validate --pptx [pptx file]\n```\n\n* Convert exam csv file into ppt file\n```\nexam_csv2pptx --sourcecsv [exam csv file] --lang [language] --title [title shown in ppt] --destpptx [pptx file]\n```\n\n* Convert ppt into pdf and images\n```\nexam_pptx2media --sourcepptx [pptx file] --destdir [dest directory storing pdf and images]\n```\n\n* Convert ppt into videos \n```\nexam_pptx2video --sourcepptx [pptx file] --destdir [dest directory storing videos] --lang es\n```\n\n### Package usage\n```\nfrom exam2pptvideo import SpanishExamPPT, SpanishExamVideo\nfrom exam2pptvideo.lib import pptx2pdf, pdf2images\n \ndef csv2pptx(sourcecsv, title, lang, destpptx):\n  _PPTS = {\n    "es": SpanishExamPPT\n  }\n\n  _PPT = _PPTS[lang]\n\n  vp = _PPT(sourcecsv, title)\n  vp.convert_to_ppt(destpptx)\n\ndef pptx2video(sourcepptx, lang, destdir):\n  _VIDEOS = {\n    "es": SpanishExamVideo\n  }\n\n  _VIDEO = _VIDEOS[lang]\n\n  ev = _VIDEO(sourcepptx)\n\n  ev.create_videos(destdir)\n\ndef pptx2pdf2images(sourcepptx, destdir):\n  pdf = pptx2pdf(sourcepptx, destdir)\n  images_len = pdf2images(pdf, destdir)\n\n```\n\n# Development\n\n### Clone project\n```\ngit clone https://github.com/qishe-ttt/exam2pptvideo \n```\n\n### Install [poetry](https://python-poetry.org/docs/)\n\n### Install dependencies\n```\npoetry update\n```\n\n### Test\n```\npoetry run pytest -rP --capture=sys\n```\nwhich run tests under `tests/*`\n\n\n### Execute\n```\npoetry run exam_pptx_validate --help\npoetry run exam_csv2pptx --help\npoetry run exam_pptx2media --help\npoetry run exam_pptx2video --help\n```\n\n### Create sphinx docs\n```\npoetry shell\ncd apidocs\nsphinx-apidoc -f -o source ../exam2pptvideo\nmake html\npython -m http.server -d build/html\n```\n\n### Host docs on github pages\n```\ncp -rf apidocs/build/html/* docs/\n```\n\n### Build\n* Change `version` in `pyproject.toml` and `exam2pptvideo/__init__.py`\n* Build python package by `poetry build`\n\n### Git commit and push\n\n### Publish from local dev env\n* Set pypi test environment variables in poetry, refer to [poetry doc](https://python-poetry.org/docs/repositories/)\n* Publish to pypi test by `poetry publish -r test`\n\n### Publish through CI \n* Github action build and publish package to [test pypi repo](https://test.pypi.org/)\n\n```\ngit tag [x.x.x]\ngit push origin master\n```\n\n* Manually publish to [pypi repo](https://pypi.org/) through [github action](https://github.com/qishe-ttt/exam2pptvideo/actions/workflows/pypi.yml)\n\n',
    'author': 'Phoenix Grey',
    'author_email': 'phoenix.grey0108@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/qishe-ttt/exam2pptvideo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
