# -*- coding: utf-8 -*-


""" Esse módulo contém todas as funções auxiliares do pacote braz. """


# Importações do braz


# Importação genérica do pacote braz
__all__ = [
    'tratar_entrada'
]


# Funções Auxiliares
def tratar_entrada(dado):
    sujeiras = '.-/ '
    for sujeira in sujeiras:
        dado = dado.replace(sujeira, '')
    return list(dado)
