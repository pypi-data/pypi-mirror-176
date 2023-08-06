# -*- coding: utf-8 -*-


""" Esse módulo contém a função gerar CNPJ do pacote. """


# Importações de módulos
import random


def cnpj(mascara: bool = True, filial: int = 1) -> str: 
    def calcular_verificador(lista):                                             
        verificador = 0                                                               
        for i, j in enumerate(lista):                                               
            verificador += (i % 8 + 2) * j
        verificador = 11 - verificador % 11                                                                                                          
        
        return verificador if (verificador < 10) else 0

    cnpj =  [filial, 0, 0, 0] + [random.randint(0, 9) for _ in range(8)]             
    for _ in range(2):
        cnpj = [calcular_verificador(cnpj)] + cnpj                           
    
    return '%s%s.%s%s%s.%s%s%s/%s%s%s%s-%s%s' % tuple(cnpj[::-1]) if mascara else '%s%s%s%s%s%s%s%s%s%s%s%s%s%s' % tuple(cnpj[::-1])
