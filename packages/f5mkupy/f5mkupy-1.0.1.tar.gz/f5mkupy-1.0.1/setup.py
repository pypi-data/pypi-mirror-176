# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['f5mkupy']

package_data = \
{'': ['*']}

install_requires = \
['cryptography']

entry_points = \
{'console_scripts': ['f5mkupy = f5mkupy.cli:cli']}

setup_kwargs = {
    'name': 'f5mkupy',
    'version': '1.0.1',
    'description': 'f5mkupy allows to encrypt and decrypt data using the format found in F5 BIG-IP bigip*.conf files with the key retrieved by f5mku -K.',
    'long_description': '# f5mkuPy\n\n[![CI Pipeline](https://github.com/simonkowallik/f5mkupy/actions/workflows/ci-pipeline.yaml/badge.svg)](https://github.com/simonkowallik/f5mkupy/actions/workflows/ci-pipeline.yaml)\n[![Maintainability](https://api.codeclimate.com/v1/badges/aed3f2ca1e1bb196e692/maintainability)](https://codeclimate.com/github/simonkowallik/f5mkupy/maintainability)\n[![Test Coverage](https://api.codeclimate.com/v1/badges/aed3f2ca1e1bb196e692/test_coverage)](https://codeclimate.com/github/simonkowallik/f5mkupy/test_coverage)\n\n_f5mkupy allows to `encrypt` and `decrypt` data using the format found in F5 BIG-IP `bigip*.conf` files with the key retrieved by `f5mku -K`._\n\n- Free software: ISC license\n- Works with Python 3.8 and up (and probably before)\n\n## What can f5mkuPy help you with?\n\n`f5mkuPy` helps you to:\n\n- decrypt\n- encrypt\n- and compare\n\nsecrets stored inline within `bigip*.conf` files.\n\nThis can be helpful in various scenarios, for example during migrations or idempotent desired state checks.\n\n`f5mkuPy` offers a command line interface and can be used as a python module as well.\n\nHave a look in the [examples/](examples/) folder for details.\n\n## Usage\n\n### A quick command line walk-through.\n\n```bash\n# f5mku -K\nF5MKU_KEY=\'BHDLd0bbao1VlwpTk1sioQ==\'\n\n# secret within a bigip*.conf file\nBIGIP_CONF_CIPHERTEXT=\'$M$bn$btwo4IWf6ZpYap4QWG8DsJqnB2xW9HLv1VOAmMeIa0U=\'\n\n# expected plaintext of that secret\nPLAINTEXT_SECRET=\'secret_encryption_key\'\n\n\n# decryption\nplaintext=$(\n    f5mkupy decrypt -k $F5MKU_KEY $BIGIP_CONF_CIPHERTEXT\n)\n[[ "$plaintext" == "$PLAINTEXT_SECRET" ]] && echo true\n# true\n\n# encryption with random salt\nciphertext=$(\n    f5mkupy encrypt -k $F5MKU_KEY $PLAINTEXT_SECRET\n)\n[[ ! "$ciphertext" == "$BIGIP_CONF_CIPHERTEXT" ]] && echo true\n# true\n\n# encryption using same salt as used in the bigip*.conf ciphertext\nsalt=$(f5mkupy extract_salt $BIGIP_CONF_CIPHERTEXT)\nciphertext=$(\n    f5mkupy encrypt -k $F5MKU_KEY -s $salt $PLAINTEXT_SECRET\n)\n[[ "$ciphertext" == "$BIGIP_CONF_CIPHERTEXT" ]] && echo true\n# true\n\n```\n\n### A quick python module walk-through.\n\n```python\nfrom f5mkupy import decrypt, encrypt, extract_salt\n\n# f5mku -K\nF5MKU_KEY=\'BHDLd0bbao1VlwpTk1sioQ==\'\n\n# secret within a bigip*.conf file\nBIGIP_CONF_CIPHERTEXT=\'$M$bn$btwo4IWf6ZpYap4QWG8DsJqnB2xW9HLv1VOAmMeIa0U=\'\n\n# expected plaintext of that secret\nPLAINTEXT_SECRET=\'secret_encryption_key\'\n\n# decryption\nplaintext = decrypt(\n        ciphertext=BIGIP_CONF_CIPHERTEXT,\n        f5mku=F5MKU_KEY\n    )\nassert plaintext == PLAINTEXT_SECRET\n\n# encryption with random salt\nciphertext = encrypt(\n        plaintext=PLAINTEXT_SECRET,\n        f5mku=F5MKU_KEY\n    )\nassert not ( ciphertext == BIGIP_CONF_CIPHERTEXT ) # what are the odds? :)\n\n# encryption using same salt as used in the bigip*.conf ciphertext\nciphertext = encrypt(\n        plaintext=PLAINTEXT_SECRET,\n        f5mku=F5MKU_KEY,\n        salt=extract_salt(ciphertext=BIGIP_CONF_CIPHERTEXT)\n    )\nassert ciphertext == BIGIP_CONF_CIPHERTEXT\n```\n\n## Disclaimer\n\nf5mkupy is not a commercial product and is not covered by any form of support, there is no contract nor SLA. Please read, understand and adhere to the license before use.\n',
    'author': 'Simon Kowallik',
    'author_email': 'sk-github@simonkowallik.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/simonkowallik/f5mkupy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
