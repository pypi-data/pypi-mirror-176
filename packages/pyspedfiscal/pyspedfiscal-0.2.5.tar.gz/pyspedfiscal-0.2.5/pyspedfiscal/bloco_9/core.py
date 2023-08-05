from typing import List
from ..models import Bloco
from .registro_9001 import Registro9001
from .registro_9999 import Registro9999


class Bloco9(Bloco):
    def __init__(self):
        self.registro_9001: Registro9001 = None
        self.registro_9999: Registro9999 = None

    @classmethod
    def ler_registros(cls, registros: List[str]) -> 'Bloco9':
        bloco = cls()

        for registro in registros:
            tipo_registro = registro[1:5].upper()

            # Nivel 1 - Registro Pai
            if tipo_registro == '9001':
                bloco.registro_9001 = Registro9001.ler_registro(registro)

            # Nivel 0 - Encerramento do arquivo
            # Ultimo Registro do arquivo
            elif tipo_registro == '9999':
                bloco.registro_9999 = Registro9999.ler_registro(registro)

        return bloco
