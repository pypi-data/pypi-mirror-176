from typing import List, Literal, Optional
from pyspedfiscal.campos import (
    CampoData, CampoDecimal, CampoInteiro, CampoAlphanumerico, CampoSerie, CampoEnumerate
)
from pydantic import Field
from typing import Literal
from pyspedfiscal.tabelas import CodSit, CodMod
from pyspedfiscal.models import Registro

from pyspedfiscal.bloco_c.registro_c101 import RegistroC101
from pyspedfiscal.bloco_c.registro_c105 import RegistroC105
from pyspedfiscal.bloco_c.registro_c110 import RegistroC110
# from pyspedfiscal.bloco_c.registro_c120 import RegistroC120
# from pyspedfiscal.bloco_c.registro_c130 import RegistroC130
# from pyspedfiscal.bloco_c.registro_c140 import RegistroC140
# from pyspedfiscal.bloco_c.registro_c160 import RegistroC160
from pyspedfiscal.bloco_c.registro_c170 import RegistroC170
# from pyspedfiscal.bloco_c.registro_c180 import RegistroC180
from pyspedfiscal.bloco_c.registro_c190 import RegistroC190
from pyspedfiscal.bloco_c.registro_c195 import RegistroC195


class IndOper(CampoEnumerate):
    """ Indicador do tipo de operação """
    entrada = '0'
    saida = '1'


class IndEmit(CampoEnumerate):
    """ Indicador do emitente do documento fiscal """
    emissao_propria = '0'
    terceiros = '1'


class IndFrt(CampoEnumerate):
    """ Indicador do tipo do frete """
    por_conta_do_remetente = '0'
    por_conta_do_destinataio = '1'
    por_conta_do_terceiro = '2'
    proprio_por_conta_do_remetente = '3'
    proprio_por_conta_do_destinatario = '4'
    sem_ocorrencia = '9'


class IndPgto(CampoEnumerate):
    """ Indicador do tipo de pagamento """
    a_vista = '0'
    a_prazo = '1'
    outros = '2'


class RegistroC100(Registro):
    """  
    NOTA FISCAL (CÓDIGO 01), NOTA FISCAL AVULSA (CÓDIGO 1B), 
    NOTA FISCAL DE PRODUTOR (CÓDIGO 04), NF-e (CÓDIGO 55) e NFC-e (CÓDIGO 65)
    """
    reg: Literal['C100']
    ind_oper: IndOper
    ind_emit: IndEmit
    cod_part: CampoAlphanumerico
    cod_mod: CodMod
    cod_sit: CodSit
    ser: CampoSerie
    num_doc: CampoInteiro
    chv_nfe: CampoInteiro
    dt_doc: CampoData
    dt_e_s: CampoData
    vl_doc: CampoDecimal
    ind_pgto: IndPgto
    vl_desc: CampoDecimal
    vl_abat_nt: CampoDecimal
    vl_merc: CampoDecimal
    ind_frt: IndFrt
    vl_frt: CampoDecimal
    vl_seg: CampoDecimal
    vl_out_da: CampoDecimal
    vl_bc_icms: CampoDecimal
    vl_icms: CampoDecimal
    vl_bc_icms_st: CampoDecimal
    vl_icms_st: CampoDecimal
    vl_ipi: CampoDecimal
    vl_pis: CampoDecimal
    vl_cofins: CampoDecimal
    vl_pis_st: CampoDecimal
    vl_cofins_st: CampoDecimal

    # Registros filhos nivel 3
    registros_c101: Optional[RegistroC101] = Field(exclude=True)
    registros_c105: Optional[RegistroC105] = Field(exclude=True)
    registros_c110: List[RegistroC110] = Field(
        default_factory=list, exclude=True)
    # registros_c120: List[RegistroC120] = Field(default_factory=list)
    # registros_c130: List[RegistroC130] = Field(default_factory=list)
    # registros_c140: List[RegistroC140] = Field(default_factory=list)
    # registros_c160: List[RegistroC160] = Field(default_factory=list)
    registros_c170: List[RegistroC170] = Field(
        default_factory=list, exclude=True)
    # registros_c180: List[RegistroC180] = Field(default_factory=list)
    registros_c190: List[RegistroC190] = Field(
        default_factory=list, exclude=True)
    registros_c195: List[RegistroC195] = Field(
        default_factory=list, exclude=True)
