from datetime import date
from pyspedfiscal.bloco_9 import Bloco9
import unittest


class TestBloco9(unittest.TestCase):

    def setUp(self) -> None:

        bloco = """
|9001|0|
|9900|0000|1|
|9900|0001|1|
|9900|0002|1|
|9900|0005|1|
|9900|0100|1|
|9900|0150|5|
|9900|0190|2|
|9900|0200|5|
|9900|0400|1|
|9900|0450|1|
|9900|0460|1|
|9900|0990|1|
|9900|B001|1|
|9900|B990|1|
|9900|C001|1|
|9900|C100|5|
|9900|C101|1|
|9900|C105|1|
|9900|C110|1|
|9900|C111|1|
|9900|C112|1|
|9900|C113|1|
|9900|C114|1|
|9900|C116|1|
|9900|C170|5|
|9900|C190|5|
|9900|C195|5|
|9900|C197|5|
|9900|C990|1|
|9900|D001|1|
|9900|D100|1|
|9900|D190|1|
|9900|D990|1|
|9900|E001|1|
|9900|E100|1|
|9900|E110|1|
|9900|E300|2|
|9900|E310|2|
|9900|E500|1|
|9900|E520|1|
|9900|E990|1|
|9900|G001|1|
|9900|G990|1|
|9900|H001|1|
|9900|H990|1|
|9900|K001|1|
|9900|K100|1|
|9900|K990|1|
|9900|1001|1|
|9900|1010|1|
|9900|1990|1|
|9900|9001|1|
|9900|9990|1|
|9900|9999|1|
|9900|9900|55|
|9990|58|
|9999|140|
""".splitlines()

        self.bloco_9 = Bloco9.ler_registros(bloco)

    def test_deve_ler_um_registro_9001(self):
        reg = self.bloco_9.registro_9001.reg
        ind_mov = self.bloco_9.registro_9001.ind_mov

        self.assertEqual(reg, '9001')
        self.assertEqual(ind_mov, '0')

    def test_deve_ler_um_registro_9999(self):
        reg = self.bloco_9.registro_9999.reg
        qtd_lin = self.bloco_9.registro_9999.qtd_lin

        self.assertEqual(reg, '9999')
        self.assertEqual(qtd_lin, 140)


if __name__ == '__main__':
    unittest.main()
