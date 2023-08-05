from datetime import date
from decimal import Decimal
from pyspedfiscal.bloco_0 import Bloco0
from pyspedfiscal.bloco_0.registro_0000 import IndAtiv, Registro0000
import unittest
from pyspedfiscal import tabelas


class TestBloco0(unittest.TestCase):

    def setUp(self) -> None:

        bloco = """
|0000|016|0|01072022|31072022|EMPRESA TESTE|14028298000152||SP|009371438460|3550308|||A|0|
|0001|0|
|0002|00|
|0005|EMPRESA TESTE|25821270|RUA EMPRESA TESTE|1111||BAIRRO EMPRESA TESTE|2499999999|||
|0015|RJ|14201122|
|0100|CONTADOR TESTE|25142702000|1-SP-111111/O-1||25805290|RUA CONTADOR|111|ENDERECO CONTADOR|BAIRRO CONTADOR|2499999999||emailcontador@contador.com.br|3550308|
|0150|1|FORNECEDOR 1|1058|03446003000141|||3301702||ENDERECO FORNECEDOR 1|1111||BAIRRO FORNECEDOR 1|
|0150|2|FORNECEDOR 2|1058|97509345000107|||3550308||ENDERECO FORNECEDOR 1|2222||BAIRRO FORNECEDOR 2|
|0150|3|FORNECEDOR 3|1058|05929208000103|||3550308||ENDERECO FORNECEDOR 1|3333||BAIRRO FORNECEDOR 3|
|0150|4|FORNECEDOR 4|1058|13992567000133|||3550308||ENDERECO FORNECEDOR 1|4444||BAIRRO FORNECEDOR 4|
|0175|10072022|11|145|
|0150|5|FORNECEDOR 5|1058|38284654000167|||3550308||ENDERECO FORNECEDOR 1|5555||BAIRRO FORNECEDOR 5|
|0175|10072022|11|145|
|0175|11072022|03|FORNECEDOR 11|
|0190|KG|KILO|
|0190|UN|UNIDADE|
|0200|1|PRODUTO 1|||UN|00|27101921||||||
|0200|2|PRODUTO 2|||KG|00|27101921||||||
|0200|3|PRODUTO 3|||KG|00|27101921||||||
|0200|4|PRODUTO 4|||KG|00|27101921||||||
|0200|5|PRODUTO 5|||KG|00|27101921||||||
|0400|1653002|Natureza Teste|
|0450|1|Informacaoo Complementar Teste|
|0460|1|Observacao Teste|
|0990|21|""".splitlines()

        self.bloco_0 = Bloco0.ler_registros(bloco)

    def test_deve_ler_um_registro_0000(self):
        registro_0000 = self.bloco_0.registro_0000

        # |0000|016|0|01072022|31072022|EMPRESA TESTE|14028298000152||SP|009371438460|3550308|||A|0|

        self.assertEqual(registro_0000.reg, '0000')
        self.assertEqual(registro_0000.cod_ver, '016')
        self.assertEqual(registro_0000.cod_fin, '0')
        self.assertEqual(registro_0000.dt_ini, date(2022, 7, 1))
        self.assertEqual(registro_0000.dt_fin, date(2022, 7, 31))
        self.assertEqual(registro_0000.nome, 'EMPRESA TESTE')
        self.assertEqual(registro_0000.cnpj, 14028298000152)
        self.assertEqual(registro_0000.cpf, None)
        self.assertEqual(registro_0000.uf, 'SP')
        self.assertEqual(registro_0000.ie, '009371438460')
        self.assertEqual(registro_0000.cod_mun, 3550308)
        self.assertEqual(registro_0000.im, None)
        self.assertEqual(registro_0000.suframa, None)
        self.assertEqual(registro_0000.ind_perfil, 'A')
        self.assertEqual(registro_0000.ind_ativ, IndAtiv.industrial)

    def test_deve_ler_um_registro_0001(self):
        registro_0001 = self.bloco_0.registro_0001

        reg = registro_0001.reg
        ind_mov = registro_0001.ind_mov

        # |0001|0|

        self.assertEqual(reg, '0001')
        self.assertEqual(ind_mov, '0')

    def test_deve_ler_um_registro_0002(self):
        registro_0002 = self.bloco_0.registro_0001.registro_0002

        reg = registro_0002.reg
        clas_estab_ind = registro_0002.clas_estab_ind

        # |0002|00|

        self.assertEqual(reg, '0002')
        self.assertEqual(clas_estab_ind, tabelas.ClassifContribIpi.industrial_transformacao)

    def test_deve_ler_um_registro_0005(self):
        registro_0005 = self.bloco_0.registro_0001.registro_0005

        reg = registro_0005.reg
        fantasia = registro_0005.fantasia
        cep = registro_0005.cep
        end = registro_0005.end
        num = registro_0005.num
        compl = registro_0005.compl
        bairro = registro_0005.bairro
        fone = registro_0005.fone
        fax = registro_0005.fax
        email = registro_0005.email

        # |0005|EMPRESA TESTE|25821270|RUA EMPRESA TESTE|1111||BAIRRO EMPRESA TESTE|2499999999|||

        self.assertEqual(reg, '0005')
        self.assertEqual(fantasia, 'EMPRESA TESTE')
        self.assertEqual(cep, 25821270)
        self.assertEqual(end, 'RUA EMPRESA TESTE')
        self.assertEqual(num, '1111')
        self.assertEqual(compl, None)
        self.assertEqual(bairro, 'BAIRRO EMPRESA TESTE')
        self.assertEqual(fone, '2499999999')
        self.assertEqual(fax, None)
        self.assertEqual(email, None)

    def test_deve_ler_um_registro_0015(self):
        registros_0015 = self.bloco_0.registro_0001.registros_0015[0]

        # |0015|RJ|14201122|

        self.assertEqual(registros_0015.reg, '0015')
        self.assertEqual(registros_0015.uf_st, 'RJ')
        self.assertEqual(registros_0015.ie_st, '14201122')

    def test_deve_ler_um_registro_0100(self):
        registro_0100 = self.bloco_0.registro_0001.registro_0100

        # |0100|CONTADOR TESTE|25142702000|1-SP-111111/O-1||25805290|RUA CONTADOR|111|ENDERECO CONTADOR|BAIRRO CONTADOR|2499999999||emailcontador@contador.com.br|3550308|

        self.assertEqual(registro_0100.reg, '0100')
        self.assertEqual(registro_0100.nome, 'CONTADOR TESTE')
        self.assertEqual(registro_0100.cpf, 25142702000)
        self.assertEqual(registro_0100.crc, '1-SP-111111/O-1')
        self.assertEqual(registro_0100.cnpj, None)
        self.assertEqual(registro_0100.cep, 25805290)
        self.assertEqual(registro_0100.end, 'RUA CONTADOR')
        self.assertEqual(registro_0100.num, '111')
        self.assertEqual(registro_0100.compl, 'ENDERECO CONTADOR')
        self.assertEqual(registro_0100.bairro, 'BAIRRO CONTADOR')
        self.assertEqual(registro_0100.fone, '2499999999')
        self.assertEqual(registro_0100.fax, None)
        self.assertEqual(registro_0100.email, 'emailcontador@contador.com.br')
        self.assertEqual(registro_0100.cod_mun, 3550308)

    def test_deve_ler_um_registro_0150(self):
        registro_0150 = self.bloco_0.registro_0001.registros_0150[0]

        # |0150|1|FORNECEDOR 1|1058|03446003000141|||3301702||ENDERECO FORNECEDOR 1|1111||BAIRRO FORNECEDOR 1|

        self.assertEqual(registro_0150.reg, '0150')
        self.assertEqual(registro_0150.cod_part, '1')
        self.assertEqual(registro_0150.nome, 'FORNECEDOR 1')
        self.assertEqual(registro_0150.cod_pais, 1058)
        self.assertEqual(registro_0150.cnpj, 3446003000141)
        self.assertEqual(registro_0150.cpf, None)
        self.assertEqual(registro_0150.ie, None)
        self.assertEqual(registro_0150.cod_mun, 3301702)
        self.assertEqual(registro_0150.suframa, None)
        self.assertEqual(registro_0150.end, 'ENDERECO FORNECEDOR 1')
        self.assertEqual(registro_0150.num, '1111')
        self.assertEqual(registro_0150.compl, None)
        self.assertEqual(registro_0150.bairro, 'BAIRRO FORNECEDOR 1')

    def test_deve_ler_um_registro_0175(self):
        registro_0175_1 = self.bloco_0.registro_0001.registros_0150[-1].registros_0175[0]
        registro_0175_2 = self.bloco_0.registro_0001.registros_0150[-1].registros_0175[1]

        # |0175|10072022|11|145|
        # |0175|11072022|03|FORNECEDOR 11|

        self.assertEqual(registro_0175_1.reg, '0175')
        self.assertEqual(registro_0175_1.dt_alt, date(2022, 7, 10))
        self.assertEqual(registro_0175_1.nr_campo, '11')
        self.assertEqual(registro_0175_1.cont_ant, '145')

        self.assertEqual(registro_0175_2.reg, '0175')
        self.assertEqual(registro_0175_2.dt_alt, date(2022, 7, 11))
        self.assertEqual(registro_0175_2.nr_campo, '03')
        self.assertEqual(registro_0175_2.cont_ant, 'FORNECEDOR 11')

    def test_deve_ler_um_registro_0200(self):
        registro_0200 = self.bloco_0.registro_0001.registros_0200[1]

        # |0200|2|PRODUTO 2|||KG|00|27101921||||||

        self.assertEqual(registro_0200.reg, '0200')
        self.assertEqual(registro_0200.cod_item, '2')
        self.assertEqual(registro_0200.descr_item, 'PRODUTO 2')
        self.assertEqual(registro_0200.cod_barra, None)
        self.assertEqual(registro_0200.cod_ant_item, None)
        self.assertEqual(registro_0200.unid_inv, 'KG')
        self.assertEqual(registro_0200.tipo_item, '00')
        self.assertEqual(registro_0200.cod_ncm, '27101921')
        self.assertEqual(registro_0200.ex_ipi, None)
        self.assertEqual(registro_0200.cod_gen, None)
        self.assertEqual(registro_0200.cod_lst, None)
        self.assertEqual(registro_0200.aliq_icms, None)
        self.assertEqual(registro_0200.cest, None)

    def test_deve_ler_um_registro_0460(self):
        registro_0460 = self.bloco_0.registro_0001.registros_0460[0]

        # |0460|1|Observacao Teste|

        self.assertEqual(registro_0460.reg, '0460')
        self.assertEqual(registro_0460.cod_obs, '1')
        self.assertEqual(registro_0460.txt, 'Observacao Teste')


if __name__ == '__main__':
    unittest.main()
