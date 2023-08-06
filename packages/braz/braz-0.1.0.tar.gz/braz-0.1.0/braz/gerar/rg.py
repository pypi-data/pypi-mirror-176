# -*- coding: utf-8 -*-


""" Esse módulo contém a função gerar RG do pacote. """


# Importações de módulos
import random


def rg(mascara: bool = True) -> str: 
    rg = [random.randint(0, 9) for _ in range(9)]
    return '%s%s.%s%s%s.%s%s%s-%s' % tuple(rg) if mascara else '%s%s%s%s%s%s%s%s%s' % tuple(rg)
