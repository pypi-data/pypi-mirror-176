from typing import Literal
from pyspedfiscal.models import Registro
from pyspedfiscal.campos import CampoEnumerate, CampoAlphanumerico, CampoDecimal, CampoInteiro


class TipoItem(CampoEnumerate):
    revenda = '00'
    materia_prima = '01'
    embalagem = '02'
    produto_em_processo = '03'
    produto_acabado = '04'
    subproduto = '05'
    produto_intermediario = '06'
    uso_e_consumo = '07'
    imobilizado = '08'
    servico = '09'
    outros_insumos = '10'
    outras = '99'


class Registro0200(Registro):
    """ TABELA DE IDENTIFICAÇÃO DO ITEM (PRODUTO E SERVIÇOS) """

    reg: Literal['0200']
    cod_item: CampoAlphanumerico
    descr_item: CampoAlphanumerico
    cod_barra: CampoAlphanumerico
    cod_ant_item: CampoAlphanumerico
    unid_inv: CampoAlphanumerico
    tipo_item: TipoItem
    cod_ncm: CampoAlphanumerico
    ex_ipi: CampoAlphanumerico
    cod_gen: CampoAlphanumerico  # TODO: Tabela 4.2.1.
    # TODO: Anexo I da Lei Complementar Federal nº 116/03.
    cod_lst: CampoAlphanumerico
    aliq_icms: CampoDecimal
    cest: CampoInteiro
