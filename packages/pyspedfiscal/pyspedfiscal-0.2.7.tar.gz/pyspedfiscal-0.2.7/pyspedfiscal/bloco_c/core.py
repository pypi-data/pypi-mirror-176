from typing import List
from ..models import Bloco
from .registro_c001 import RegistroC001
from .registro_c100 import RegistroC100
from .registro_c101 import RegistroC101
from .registro_c105 import RegistroC105
from .registro_c110 import RegistroC110
from .registro_c111 import RegistroC111
from .registro_c112 import RegistroC112
from .registro_c113 import RegistroC113
from .registro_c114 import RegistroC114
from .registro_c115 import RegistroC115
from .registro_c116 import RegistroC116
from .registro_c120 import RegistroC120
from .registro_c130 import RegistroC130
from .registro_c140 import RegistroC140
from .registro_c160 import RegistroC160
from .registro_c170 import RegistroC170
from .registro_c180 import RegistroC180
from .registro_c190 import RegistroC190
from .registro_c195 import RegistroC195
from .registro_c197 import RegistroC197


class BlocoC(Bloco):
    def __init__(self):
        self.registro_c001: RegistroC001 = None

    @classmethod
    def ler_registros(cls, registros: List[str]) -> 'BlocoC':
        bloco = cls()

        for registro in registros:
            tipo_registro = registro[1:5].upper()

            # Nivel 1 - Registro Pai
            if tipo_registro == 'C001':
                bloco.registro_c001 = RegistroC001.ler_registro(registro)

            # Nivel 2 - Filho de C001
            elif tipo_registro == 'C100':
                registro_c100 = RegistroC100.ler_registro(registro)
                bloco.registro_c001.registros_c100.append(registro_c100)

            # Nivel 3 - Filho de C100
            elif tipo_registro == 'C101':
                registro_c100.registros_c101 = RegistroC101.ler_registro(
                    registro)

            # Nivel 3 - Filho de C100
            elif tipo_registro == 'C105':
                registro_c100.registros_c105 = RegistroC105.ler_registro(
                    registro)

            # Nivel 3 - Filho de C100
            elif tipo_registro == 'C110':
                registro_c110 = RegistroC110.ler_registro(registro)
                registro_c100.registros_c110.append(registro_c110)

            # Nivel 4 - Filho de C110
            elif tipo_registro == 'C111':
                registro_c111 = RegistroC111.ler_registro(registro)
                registro_c110.registros_c111.append(registro_c111)

            # Nivel 4 - Filho de C110
            elif tipo_registro == 'C112':
                registro_c112 = RegistroC112.ler_registro(registro)
                registro_c110.registros_c112.append(registro_c112)

            # Nivel 4 - Filho de C110
            elif tipo_registro == 'C113':
                registro_c113 = RegistroC113.ler_registro(registro)
                registro_c110.registros_c113.append(registro_c113)

            # Nivel 4 - Filho de C110
            elif tipo_registro == 'C114':
                registro_c114 = RegistroC114.ler_registro(registro)
                registro_c110.registros_c114.append(registro_c114)

            # Nivel 4 - Filho de C110
            elif tipo_registro == 'C115':
                registro_c115 = RegistroC115.ler_registro(registro)
                registro_c110.registros_c115.append(registro_c115)

            # Nivel 4 - Filho de C110
            elif tipo_registro == 'C116':
                registro_c116 = RegistroC116.ler_registro(registro)
                registro_c110.registros_c116.append(registro_c116)

            # Nivel 3 - Filho de C100
            elif tipo_registro == 'C170':
                registro_c170 = RegistroC170.ler_registro(registro)
                registro_c100.registros_c170.append(registro_c170)

            # Nivel 3 - Filho de C100
            elif tipo_registro == 'C190':
                registro_c190 = RegistroC190.ler_registro(registro)
                registro_c100.registros_c190.append(registro_c190)

            # Nivel 3 - Filho de C100
            elif tipo_registro == 'C195':
                registro_c195 = RegistroC195.ler_registro(registro)
                registro_c100.registros_c195.append(registro_c195)

            # Nivel 4 - Filho de C195
            elif tipo_registro == 'C197':
                registro_c197 = RegistroC197.ler_registro(registro)
                registro_c195.registros_c197.append(registro_c197)

        return bloco
