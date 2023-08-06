# -*- coding: utf-8 -*-


""" Esse módulo contém a função validar CNPJ do pacote. """


# Importação de módulos
import re


def cnpj(dado: str) -> bool: 
    cnpj = ''.join(re.findall('\d', str(dado)))
    if (not cnpj) or (len(cnpj) < 14):
        return False

    verificador = list(map(int, cnpj))
    novo = verificador[:12]

    prod = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    while len(novo) < 14:
        r = sum([x * y for x, y in zip(novo, prod)]) % 11
        f = 11 - r if (r > 1) else 0
        novo.append(f)
        prod.insert(0, 6)

    return True if (novo == verificador) else False
