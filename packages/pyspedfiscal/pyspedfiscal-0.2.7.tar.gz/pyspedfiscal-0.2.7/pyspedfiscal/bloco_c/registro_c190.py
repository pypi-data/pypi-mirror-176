from typing import List, Literal
from pyspedfiscal.campos import CampoDecimal, CampoInteiro, CampoAlphanumerico
from pydantic import Field
from pyspedfiscal.models import Registro


class RegistroC190(Registro):
    """ Registro Analítico do Documento (código 01, 1B, 04, 55 e 65)  """
    reg: Literal['C190']
    cst_icms: CampoInteiro
    cfop: CampoInteiro
    aliq_icms: CampoDecimal
    vl_opr: CampoDecimal
    vl_bc_icms: CampoDecimal
    vl_icms: CampoDecimal
    vl_bc_icms_st: CampoDecimal
    vl_icms_st: CampoDecimal
    vl_red_bc: CampoDecimal
    vl_ipi: CampoDecimal
    cod_obs: CampoAlphanumerico
