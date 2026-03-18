*[Read in English](README.md)*

# django-edne-cep

[![PyPI version](https://img.shields.io/pypi/v/django-edne-cep.svg)](https://pypi.org/project/django-edne-cep/)
[![CI](https://github.com/cauethenorio/django-edne-cep/actions/workflows/lint-and-test.yml/badge.svg)](https://github.com/cauethenorio/django-edne-cep/actions/workflows/lint-and-test.yml)
[![Coverage](https://codecov.io/gh/cauethenorio/django-edne-cep/graph/badge.svg)](https://codecov.io/gh/cauethenorio/django-edne-cep)

Habilita consulta de CEP em seu app Django com banco de dados local.
Utiliza o [edne-correios-loader](https://github.com/cauethenorio/edne-correios-loader) para popular o banco de dados com
os dados eDNE dos Correios, eliminando dependência de APIs externas.

- Consultas em banco de dados local, sem chamadas a APIs externas, sem latência de rede
- Cache com proteção contra stampede (baseado em sentinel, armazena resultados não encontrados também)
- Campo de formulário com validação de formato de CEP e preenchimento automático de endereço
- Integração com o admin do Django (opcional)
- Nomes de tabelas, alias de banco de dados e backend de cache configuráveis

![Demo de Consulta de CEP](https://raw.githubusercontent.com/cauethenorio/django-edne-cep/main/docs/images/cep-lookup.gif)

*Consulta de CEP com HTMX no app de exemplo*

![Integração com Admin](https://raw.githubusercontent.com/cauethenorio/django-edne-cep/main/docs/images/admin.png)

*Admin do Django exibindo dados de CEP*

## Início Rápido

**Passo 1: Instalar**

```bash
pip install django-edne-cep
```

**Passo 2: Adicionar ao `INSTALLED_APPS`**

```python
INSTALLED_APPS = [
    ...
    "django_edne_cep",
]
```

**Passo 3: Carregar os dados de CEP**

```bash
python manage.py load_edne_cep --auto-download
```

Isso faz o download do dataset eDNE dos Correios (~350 MB) e popula o banco de dados local. Execuções subsequentes
reutilizam o arquivo em cache.

**Usar:**

```python
from django_edne_cep import lookup_cep

cep = lookup_cep("01310-100")
if cep:
    print(f"{cep.logradouro}, {cep.municipio}/{cep.uf}")
    # "Avenida Paulista, São Paulo/SP"
```

## Referência da API

### `def lookup_cep(cep_str: str) -> Cep | None`

Consulta um CEP no banco de dados local. Aceita os formatos `"01310-100"` e `"01310100"`.

- Lança `ValidationError` para entrada malformada (formato de CEP inválido).
- Retorna `None` quando o CEP não é encontrado no banco de dados (formato válido, mas não presente nos dados eDNE).
- Os resultados são armazenados em cache usando o backend de cache configurado.

```python
from django_edne_cep import lookup_cep
from django.core.exceptions import ValidationError

cep = lookup_cep("01310-100")  # aceita "01310-100" ou "01310100"
if cep:
    print(f"{cep.logradouro}, {cep.municipio}/{cep.uf}")

try:
    lookup_cep("ABC")  # lança ValidationError para entrada malformada
except ValidationError:
    pass
```

A instância `Cep` retornada possui os seguintes campos:

```python
cep.cep  # "01310100"  (8 dígitos, sem hífen)
cep.cep_formatado  # "01310-100" (property)
cep.logradouro  # str | None
cep.complemento  # str | None
cep.bairro  # str | None
cep.municipio  # str
cep.municipio_cod_ibge  # int
cep.uf  # str (2 caracteres, ex: "SP")
cep.nome  # str | None
cep.as_dict()  # dict com todos os campos acima
```

---

### `CepFormField`

Uma subclasse de `CharField` que valida o formato do CEP e retorna uma instância de `Cep` em `clean()`.

- Aceita os formatos de entrada `"00000000"` ou `"00000-000"`.
- Lança `ValidationError` com o código `"cep_not_found"` quando o CEP não está no banco de dados.
- `form.cleaned_data["cep"]` é uma instância de `Cep`, não uma string.

```python
from django import forms
from django_edne_cep import CepFormField


class EnderecoForm(forms.Form):
    cep = CepFormField()
    logradouro = forms.CharField(required=False)
    municipio = forms.CharField(required=False)


# Em uma view:
form = EnderecoForm(request.POST)
if form.is_valid():
    cep_obj = form.cleaned_data["cep"]  # instância de Cep
    print(cep_obj.logradouro, cep_obj.municipio, cep_obj.uf)
```

---

### `validate_cep_format`

Um `RegexValidator` do Django que aceita os formatos `"00000000"` e `"00000-000"`. Lança `ValidationError` com o código
`"invalid_cep_format"` em caso de falha.

```python
from django_edne_cep import validate_cep_format

validate_cep_format("01310-100")  # passa silenciosamente
validate_cep_format("01310100")  # passa silenciosamente
validate_cep_format("ABC")  # lança ValidationError
```

Use diretamente em qualquer `CharField` ou `Field` que deva aceitar valores de CEP sem acionar uma consulta ao banco de
dados.

---

### `register_admin(site: AdminSite | None = None) -> None`

Registra o modelo `Cep` com um `CepAdmin` somente leitura no site de admin fornecido. O caso de uso padrão não requer
chamada manual. Defina `EDNE_CEP["ADMIN_ENABLED"] = True` nas configurações do Django.

`register_admin()` é chamado automaticamente quando `django_edne_cep.admin` é importado com `ADMIN_ENABLED=True`. A
chamada explícita só é necessária para um `AdminSite` personalizado.

```python
# Uso padrão, definir nas configurações do Django:
EDNE_CEP = {
    "ADMIN_ENABLED": True,
}

# Somente para uso com AdminSite personalizado:
from django_edne_cep import register_admin

register_admin(site=my_custom_site)
```

## Configuração

Todas as configurações ficam no dict `EDNE_CEP` no arquivo de configurações do Django:

```python
EDNE_CEP = {
    "CACHE_TIMEOUT": 7200,
    "ADMIN_ENABLED": True,
}
```

| Configuração     | Tipo          | Padrão      | Descrição                                                        |
|------------------|---------------|-------------|------------------------------------------------------------------|
| `TABLE_NAMES`    | `dict`        | veja abaixo | Sobrescreve nomes individuais de tabelas eDNE                    |
| `TABLE_SET`      | `str \| None` | `None`      | Carrega apenas um subconjunto de tabelas (ex: `"cep"`)           |
| `EDNE_SOURCE`    | `str \| None` | `None`      | Caminho ou URL para o arquivo zip eDNE; `None` solicita download |
| `DATABASE_ALIAS` | `str`         | `"default"` | Alias de banco de dados do Django para as tabelas de CEP         |
| `DATABASE_URL`   | `str \| None` | `None`      | URL direta de banco de dados (substitui `DATABASE_ALIAS`)        |
| `CACHE_TIMEOUT`  | `int`         | `3600`      | TTL do cache em segundos; `0` desativa o cache                   |
| `CACHE_ALIAS`    | `str`         | `"default"` | Alias de cache do Django para consultas de CEP                   |
| `ADMIN_ENABLED`  | `bool`        | `False`     | Registra os modelos de CEP no admin do Django                    |

**`TABLE_NAMES` padrão:**

```python
TABLE_NAMES = {
    "cep_unificado": "edne_cep",
    "log_localidade": "edne_localidade",
    "log_bairro": "edne_bairro",
    "log_cpc": "edne_caixa_postal",
    "log_logradouro": "edne_logradouro",
    "log_grande_usuario": "edne_grande_usuario",
    "log_unid_oper": "edne_unidade_operacional",
}
```

Sobrescreva entradas individuais para mapear os nomes de tabela eDNE para seus próprios nomes de tabela.

## Admin

Habilite o admin somente leitura do Django para dados de CEP:

```python
# settings.py
EDNE_CEP = {
    "ADMIN_ENABLED": True,
}
```

O `CepAdmin` é registrado automaticamente quando `django_edne_cep.admin` é importado. Suporta busca por texto completo
por CEP, nome do logradouro, bairro e município, além de filtros por estado (UF) e presença de campo.

Para um `AdminSite` personalizado, chame `register_admin(site=my_site)` explicitamente após definir
`ADMIN_ENABLED = True`.

![Integração com Admin](https://raw.githubusercontent.com/cauethenorio/django-edne-cep/main/docs/images/admin.png)

## App de Exemplo

O diretório `example/` contém um projeto Django independente com um formulário de preenchimento automático de CEP com
HTMX: digite um CEP e os campos de endereço são preenchidos automaticamente sem recarregar a página.

Veja [example/README.md](example/README.md) para instruções completas sobre como executar localmente.

## Licença

[MIT](LICENSE)
