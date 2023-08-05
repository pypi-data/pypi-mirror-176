from decimal import Decimal
from pyspedfiscal.bloco_c import BlocoC
import unittest


class TestBlocoC(unittest.TestCase):

    def setUp(self) -> None:

        bloco = """
|C001|0|
|C100|1|1|1|55|00|1|1|33220714028298000152550010000000011000147724|27072022|27072022|41961,29|2|0|0|41961,29|0|0|0|0|0|0|0|0|0|0|0|0|0|
|C101|100|20|80|
|C105|0|RJ|
|C110|1|Descrição Complementar Teste|
|C111|Processo Teste|0|
|C112|0|RJ|3|1000|100|01072022|31072022|
|C113|0|0|1|01|001||1|01072022||
|C114|02|1|1|1|01072022|
|C116|59|1|33220714028298000152570010000002110001477205|1|01072022|
|C170|2|1||381,563|UN|2896,06|0|0|060|5101|1653002|0|0|0|0|0|0||||0|0|0|49|2896,06|0,35|0|0|10,14|49|2896,06|0,35|0|0|10,14|4212|0|
|C190|060|5101|0|0|0|0|0|0|0|0||
|C195|1|FECP referente ao diferencial de aliquotas|
|C197|SP10090718|FECP referente ao diferencial de aliquotas||3256,23|0|596,98|0|
|C990|35|""".splitlines()

        self.bloco_c = BlocoC.ler_registros(bloco)

    def test_deve_ler_um_registro_c100(self):

        chv_nfe = self.bloco_c.registro_c001.registros_c100[0].chv_nfe
        vl_doc = self.bloco_c.registro_c001.registros_c100[0].vl_doc
        reg = self.bloco_c.registro_c001.registros_c100[0].reg

        self.assertEqual(reg, 'C100')
        self.assertEqual(
            chv_nfe, 33220714028298000152550010000000011000147724)
        self.assertEqual(
            vl_doc, Decimal('41961.29'))

    def test_deve_ler_um_registro_c101(self):
        vl_fcp_uf_dest = self.bloco_c.registro_c001.registros_c100[0].registros_c101.vl_fcp_uf_dest
        vl_icms_uf_dest = self.bloco_c.registro_c001.registros_c100[
            0].registros_c101.vl_icms_uf_dest
        vl_icms_uf_rem = self.bloco_c.registro_c001.registros_c100[0].registros_c101.vl_icms_uf_rem

        self.assertEqual(vl_fcp_uf_dest, Decimal('100'))
        self.assertEqual(vl_icms_uf_dest, Decimal('20'))
        self.assertEqual(vl_icms_uf_rem, Decimal('80'))
        
    def test_deve_ler_um_registro_c105(self):
        oper = self.bloco_c.registro_c001.registros_c100[0].registros_c105.oper
        uf = self.bloco_c.registro_c001.registros_c100[0].registros_c105.uf

        self.assertEqual(oper, '0')
        self.assertEqual(uf, 'RJ')


if __name__ == '__main__':
    unittest.main()
