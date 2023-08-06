# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['braz',
 'braz.cifrar',
 'braz.criptografar',
 'braz.decifrar',
 'braz.descriptografar',
 'braz.gerar',
 'braz.manipular',
 'braz.validar']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'braz',
    'version': '0.1.0',
    'description': '🎲 Gerador, validador, cifras, criptografias e manipulação de strings.',
    'long_description': '<div id="título" align="center">\n    <img width="400px" alt="Braz - Gerador & Validador" src="https://raw.githubusercontent.com/dev-macb/braz/master/.github/assets/images/logo-nome.png"/>\n</div>\n\n\n---\n\n\n<h2 id="objetivo" align="left">🎯 Objetivo</h2>\n\n<p id="txt-contribuições" align="left">\n    O <strong>Braz</strong> é uma aplicação que disponibiliza diversas funcionalidades com o intuito de auxiliar os desenvolvedores nos projetos que necessitam da geração de dados randômicos válidos dos principais documentos pessoais do Brasil, bem como sua validação. Além do mais, o software trata cifras, criptografias, manipulação de strings e outras peculiaridades. Com o mínimo de configuração, o Braz pode ser utilizado como uma ferramenta de linha de comando para operações simples e rápidas ou sendo implementada diretamente no código-fonte como um módulo Python. \n</p>\n\n\n<h3 id="divisor" align="center">🔷</h3>\n',
    'author': 'Miguel Alves Cordeiro Braz',
    'author_email': 'dev.macb@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
