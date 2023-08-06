from typing import Literal
from pyspedfiscal.models import Registro
from pyspedfiscal.campos import CampoEnumerate


class IndMov(CampoEnumerate):
    """ Indicador de movimento """
    com_movimento = '0'
    sem_movimento = '1'


class Registro9001(Registro):
    """ Abertura do Bloco 9"""
    reg: Literal['9001']
    ind_mov: IndMov
