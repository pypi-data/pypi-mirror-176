# -*- coding: utf-8 -*-


""" Esse módulo contém a função gerar CPF do pacote. """


# Importações de módulos
import random


def cpf(mascara: bool = True) -> str: 
    cpf = [random.randint(0, 9) for _ in range(9)]                                                           
    for _ in range(2):
        verificador = sum([(len(cpf) + 1 - i) * v for i, v in enumerate(cpf)]) % 11
        cpf.append(11 - verificador if (verificador > 1) else 0)  
    
    return '%s%s%s.%s%s%s.%s%s%s-%s%s' % tuple(cpf) if mascara else '%s%s%s%s%s%s%s%s%s%s%s' % tuple(cpf)
