# -*- coding: utf-8 -*-


""" Esse módulo contém o construtor do módulo gerar do pacote. """


# Importações do braz
from braz.gerar.rg import rg
from braz.gerar.ie import ie
from braz.gerar.cpf import cpf
from braz.gerar.cnpj import cnpj
from braz.gerar.senha import senha
from braz.gerar.renavam import renavam
from braz.gerar.pis_pasep import pis_pasep
from braz.gerar.titulo_eleitor import titulo_eleitor


# Importação genérica do pacote braz
__all__ = [
    'rg',
    'ie',
    'cpf',
    'cnpj',
    'senha',
    'renavam',
    'pis_pasep',
    'titulo_eleitor'
]
