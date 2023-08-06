# -*- coding: utf-8 -*-


""" Esse módulo contém a função gerar Senha do pacote. """


# Importações de módulos
import random
import string


def senha(tamanho: int = 10, semLetras = False, semNumeros = False, semEspeciais = False) -> str: 
    senha = ''
    conjunto_digitos = ('' if semLetras else string.ascii_letters) + ('' if semNumeros else string.digits) + ('' if semEspeciais else string.punctuation)
    for _ in range(tamanho):
        senha += random.choice(conjunto_digitos) 

    return senha
