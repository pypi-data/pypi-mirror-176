# PySpedFiscal

Lê e serializa um arquivo do tipo Sped Fiscal

### Exemplo

#### Lendo um arquivo:

```python
# Importe a classe SpedFiscal
from pyspedfiscal import SpedFiscal

# Utilize o metodo da classe `importar` para carregar um arquivo sped
sped_fiscal = SpedFiscal.importar('caminho_arquivo')

# Utilize a hierarquia do arquivo para percorrer os registros
registros_0200 = sped_fiscal.bloco_0.resgistro_0001.registros_0200

for registro in registros_0200:
  ...

```

#### Lendo um bloco:

```python

from pyspedfiscal.bloco_0 import Bloco0

bloco = """
|0000|016|0|01072022|31072022|EMPRESA TESTE|14028298000152||SP|009371438460|3550308|||A|0|
|0001|0|
|0002|00|
|0005|EMPRESA TESTE|25821270|RUA EMPRESA TESTE|1111||BAIRRO EMPRESA TESTE|2499999999|||
...
"""

registros = bloco.splitlines()

bloco_0 = Bloco0.ler_registros(registros)
```

#### Lendo um Registro

```python
from pyspedfiscal.bloco_0.registro_0000 import Registro0000

registro = "|0000|016|0|01072022|31072022|EMPRESA TESTE|14028298000152||SP|009371438460|3550308|||A|0|"

registro_0000 = Registro0000.ler_registro(registro)
```

### Registros Implementados

| Bloco 0 | Bloco B | Bloco C | Bloco D | Bloco E | Bloco G | Bloco H | Bloco G | Bloco K | Bloco 1 | Bloco 9 |
| ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- |
| 0000    |         | C001    |         | E001    |         |         |         |         |         | 9001    |
| 0001    |         | C100    |         | E100    |         |         |         |         |         | 9999    |
| 0002    |         | C101    |         | E110    |         |         |         |         |         |         |
| 0005    |         | C105    |         | E115    |         |         |         |         |         |         |
| 0015    |         | C110    |         |         |         |         |         |         |         |         |
| 0100    |         | C111    |         |         |         |         |         |         |         |         |
| 0150    |         | C112    |         |         |         |         |         |         |         |         |
| 0175    |         | C113    |         |         |         |         |         |         |         |         |
|         |         | C114    |         |         |         |         |         |         |         |         |
|         |         | C115    |         |         |         |         |         |         |         |         |
|         |         | C116    |         |         |         |         |         |         |         |         |
|         |         | C120    |         |         |         |         |         |         |         |         |
|         |         | C130    |         |         |         |         |         |         |         |         |
|         |         | C140    |         |         |         |         |         |         |         |         |
|         |         | C160    |         |         |         |         |         |         |         |         |
|         |         | C170    |         |         |         |         |         |         |         |         |
|         |         | C180    |         |         |         |         |         |         |         |         |
|         |         | C190    |         |         |         |         |         |         |         |         |
|         |         | C195    |         |         |         |         |         |         |         |         |
|         |         | C197    |         |         |         |         |         |         |         |         |

### Instalação

- `pip install pyspedfiscal`

### Dependencias

- Pydantic
