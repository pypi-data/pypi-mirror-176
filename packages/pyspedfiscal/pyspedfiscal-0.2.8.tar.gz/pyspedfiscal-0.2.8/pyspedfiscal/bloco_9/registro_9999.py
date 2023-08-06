from typing import Literal
from pyspedfiscal.models import Registro
from pyspedfiscal.campos import CampoInteiro


class Registro9999(Registro):
    """ Abertura do Bloco 9"""
    reg: Literal['9999']
    qtd_lin: CampoInteiro
