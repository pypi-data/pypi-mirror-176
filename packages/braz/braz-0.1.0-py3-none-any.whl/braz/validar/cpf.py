# -*- coding: utf-8 -*-


""" Esse módulo contém a função validar CPF do pacote. """


# Importação de módulos
import re


def cpf(dado: str) -> bool: 
    cpf = ''.join(re.findall('\d', str(dado)))
    if (not cpf) or (len(cpf) < 11):
        return False

    verificador = list(map(int, cpf))
    novo = verificador[:9]

    while len(novo) < 11:
        r = sum([(len(novo) + 1 - i) * v for i, v in enumerate(novo)]) % 11
        f = 11 - r if (r > 1) else 0
        novo.append(f)

    return True if (novo == verificador) else False
