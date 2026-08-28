# 📖 Apostila Ghanor Codex

## Construindo um Gerenciador de Fichas e Campanhas de RPG — do repositório ao deploy

> **Sistema:** A Lenda de Ghanor RPG (base Tormenta 20)
> **Stack:** Python 3.12 · Django 5 · DRF · HTMX · Alpine.js · Tailwind · PostgreSQL 16 · Docker Compose · Caddy
> **Metodologia:** TDD com pytest · Gestão de pacotes com `uv`
> **Referência de arquitetura:** `docs/adr/ADR-001-arquitetura.md`

---

## Como usar esta apostila

Cada parte segue a mesma estrutura:

1. **🧠 Conceitos** — o que você precisa entender antes de digitar qualquer código, e *por quê* as coisas são assim.
2. **🔨 Como montar** — o passo a passo recomendado, com os comandos exatos.
3. **📜 Exemplo de referência** — código completo e comentado que você pode usar como gabarito.
4. **⚔️ Exercícios** — desafios no estilo TDD: escreva o teste primeiro, veja falhar, implemente, veja passar.

A ordem das partes foi pensada para o aprendizado: cada uma depende apenas do que veio antes. **Não pule partes** — a tentação de ir direto para o frontend é grande, mas a fundação é o que separa um projeto de portfólio de um projeto de tutorial.

**Convenção de comandos:** tudo roda com `uv run` (você vai entender o porquê na Parte 2). Quando aparecer `$`, é o seu terminal.

---

# PARTE 1 — O Repositório: sua vitrine e sua fundação

## 🧠 Conceitos

### Por que a organização do repo importa tanto?

Quando um recrutador ou outro dev abre seu repositório, ele forma uma opinião em **30 segundos** — antes de ler qualquer linha de código. O que ele olha:

1. **README** — o projeto se explica sozinho?
2. **Estrutura de pastas** — reflete uma arquitetura pensada ou é uma gaveta de meias?
3. **Histórico de commits** — mensagens descritivas ou "fix", "fix2", "agora vai"?
4. **Presença de testes** — existe pasta `tests/`? Existe CI rodando?
5. **Documentação de decisões** — ADRs mostram maturidade rara até em devs sêniores.

### Anatomia de um repositório profissional

```
ghanor-codex/
├── .github/
│   └── workflows/
│       └── ci.yml              # Pipeline de integração contínua
├── docs/
│   ├── adr/
│   │   └── ADR-001-arquitetura.md   # Decisões arquiteturais versionadas
│   └── img/                    # Diagramas, screenshots para o README
├── src/
│   └── ghanor_codex/           # Código-fonte do projeto (src layout)
├── tests/                      # Testes espelham a estrutura de src/
├── scripts/                    # Scripts utilitários (seed do banco, etc.)
├── compose.yaml                # Orquestração Docker (Parte 10)
├── pyproject.toml              # Configuração do projeto Python (Parte 2)
├── .gitignore
├── .env.example                # Modelo das variáveis de ambiente (NUNCA o .env real!)
├── LICENSE
└── README.md
```

### Por que cada estrutura existe

**`src/` layout (em vez de código na raiz).** Colocar o pacote dentro de `src/` força você a *instalar* o projeto para testá-lo, em vez de depender de imports acidentais do diretório atual. Isso pega bugs de empacotamento cedo. É a recomendação oficial da Python Packaging Authority.

**`tests/` fora de `src/`.** Testes não são código de produção — não devem ser distribuídos junto com o pacote. Mantê-los separados também deixa claro o espelhamento: `src/ghanor_codex/dominio/atributos.py` ↔ `tests/dominio/test_atributos.py`.

**`docs/adr/`.** Um ADR (Architecture Decision Record) registra *por que* uma decisão foi tomada, com as alternativas consideradas. Daqui a 8 meses, quando você se perguntar "por que mesmo eu não usei MongoDB?", a resposta estará lá. Em entrevista, é ouro: você aponta para o documento em vez de tentar lembrar.

**`.env.example` versionado, `.env` ignorado.** Segredos (senhas de banco, `SECRET_KEY` do Django) **nunca** entram no Git. O `.env.example` documenta *quais* variáveis existem, sem os valores reais. Quem clona o repo copia para `.env` e preenche. Vazamento de segredo em repositório público é um dos erros mais comuns — e mais eliminatórios — em portfólios.

**`.github/workflows/`.** CI (Integração Contínua) roda seus testes automaticamente a cada push. O selo verde de "build passing" no README comunica confiabilidade.

### Commits: a narrativa do projeto

Adote **Conventional Commits** desde o primeiro commit:

```
feat: adiciona cálculo de modificador de atributo
fix: corrige bônus racial de elfo aplicado duas vezes
test: cobre casos extremos de distribuição de pontos
docs: adiciona ADR-001 de arquitetura
refactor: extrai validação de passo para classe própria
chore: configura ruff e pytest no pyproject
```

O prefixo categoriza a mudança; a mensagem, no imperativo, descreve *o que o commit faz* quando aplicado. O histórico vira uma linha do tempo legível do projeto — e recrutadores olham histórico.

### Branches: simples, porque você é um só

Para dev solo, **GitHub Flow** basta:

- `main` sempre estável (testes passando).
- Cada funcionalidade em uma branch: `feat/wizard-atributos`, `fix/bonus-racial-duplicado`.
- Merge via Pull Request **para você mesmo** — parece bobo, mas o PR roda a CI antes do merge e cria um registro revisável. É exatamente o fluxo que você usará em equipe.

## 🔨 Como montar

```bash
# 1. Crie o repositório no GitHub (ghanor-codex, público, com licença MIT)
#    e clone:
$ git clone git@github.com:SEU_USUARIO/ghanor-codex.git
$ cd ghanor-codex

# 2. Estrutura de pastas:
$ mkdir -p src/ghanor_codex tests docs/adr docs/img scripts .github/workflows

# 3. Arquivos base:
$ touch README.md .env.example .gitignore
$ touch src/ghanor_codex/__init__.py tests/__init__.py

# 4. Copie o ADR-001 para dentro do repo:
$ cp ~/Downloads/ADR-001-arquitetura-ghanor-codex.md docs/adr/ADR-001-arquitetura.md

# 5. Primeiro commit:
$ git add .
$ git commit -m "chore: estrutura inicial do repositório"
$ git push origin main
```

## 📜 Exemplo de referência

### `.gitignore`

```gitignore
# Python
__pycache__/
*.py[cod]
.venv/
*.egg-info/
.pytest_cache/
.ruff_cache/
htmlcov/
.coverage

# Segredos e ambiente — NUNCA versionar
.env

# Django
db.sqlite3
staticfiles/
media/

# Editor e SO
.vscode/
.idea/
.DS_Store
```

### `README.md` (esqueleto)

```markdown
# ⚔️ Ghanor Codex

Gerenciador de fichas e campanhas para **A Lenda de Ghanor RPG** (Tormenta 20).

![CI](https://github.com/SEU_USUARIO/ghanor-codex/actions/workflows/ci.yml/badge.svg)

## O que ele faz

- 🧙 Criação guiada de fichas: raça, classe e origem alteram atributos
  automaticamente (elfo → +2 Carisma), seguindo os 8 passos do Tormenta 20
- ❤️ Gestão em sessão: PV, PM, inventário, condições, subida de nível
- 📚 Consulta instantânea de magias e habilidades da ficha
- 🗺️ Organização de campanhas e sessões

## Stack

Django 5 · DRF · HTMX · Alpine.js · Tailwind · PostgreSQL 16 (JSONB) ·
Docker Compose · Caddy — decisões documentadas em [`docs/adr/`](docs/adr/).

## Rodando localmente

​```bash
cp .env.example .env   # preencha as variáveis
docker compose up -d db
uv sync
uv run manage.py migrate
uv run manage.py runserver
​```

## Testes

​```bash
uv run pytest
​```
```

### `.env.example`

```bash
# Django
DJANGO_SECRET_KEY=troque-por-uma-chave-segura
DJANGO_DEBUG=true
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL
POSTGRES_DB=ghanor
POSTGRES_USER=ghanor
POSTGRES_PASSWORD=troque-esta-senha
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

## ⚔️ Exercícios

1. Crie o repositório com a estrutura acima e faça 3 commits seguindo Conventional Commits.
2. No README, escreva a seção "O que ele faz" com as suas palavras — é o seu *pitch*.
3. Abra sua primeira branch (`docs/adr-001`), adicione o ADR, abra um PR para você mesmo e faça o merge.

---

# PARTE 2 — Ambiente Python moderno com `uv`

## 🧠 Conceitos

### O problema que o `uv` resolve

Todo projeto Python precisa de: (a) uma versão específica do Python, (b) um ambiente virtual isolado, (c) dependências com versões travadas para builds reproduzíveis. Historicamente isso exigia `pyenv` + `venv` + `pip` + `pip-tools`, quatro ferramentas com quatro sintaxes.

O **`uv`** unifica tudo, e é ordens de magnitude mais rápido. Os comandos que você vai usar 95% do tempo:

| Comando | O que faz |
|---|---|
| `uv init` | Cria o `pyproject.toml` |
| `uv add django` | Adiciona dependência (e atualiza o lock) |
| `uv add --dev pytest` | Dependência só de desenvolvimento |
| `uv sync` | Instala tudo conforme o `uv.lock` |
| `uv run <cmd>` | Roda um comando *dentro* do ambiente do projeto |

### `pyproject.toml`: o centro de gravidade

Um único arquivo declara: metadados do projeto, dependências, e configuração das ferramentas (pytest, ruff). Antes, isso ficava espalhado em `setup.py`, `requirements.txt`, `setup.cfg`, `pytest.ini`... O `pyproject.toml` é o padrão moderno (PEP 621).

### `uv.lock`: reprodutibilidade

O `pyproject.toml` diz "quero Django ≥ 5.0"; o `uv.lock` registra *exatamente* qual versão de cada pacote (incluindo dependências das dependências) foi instalada. **Versione o lock**: é ele que garante que o projeto rode igual no seu notebook, no home lab e na CI.

### Qualidade de código: ruff

O **ruff** é linter + formatador num binário só (substitui flake8, isort e black). Linter aponta erros e más práticas; formatador padroniza o estilo — e discussão de estilo é a maior fonte de bikeshedding em código. Automatize e esqueça.

### pytest e a disciplina do TDD

O ciclo TDD que esta apostila segue em **todas** as partes:

1. 🔴 **Red** — escreva um teste que descreve o comportamento desejado. Rode. Ele falha (o código não existe).
2. 🟢 **Green** — escreva o código *mínimo* que faz o teste passar.
3. 🔵 **Refactor** — melhore o código com a segurança de que os testes te protegem.

Por que isso importa aqui, especificamente? Porque **regras de RPG são o caso de uso perfeito para TDD**: o livro de regras *é* a especificação. "Elfo recebe +2 Carisma" é literalmente um caso de teste esperando para ser escrito.

## 🔨 Como montar

```bash
# 1. Instale o uv (https://docs.astral.sh/uv/):
$ curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Na raiz do repo, inicialize:
$ uv init --python 3.12

# 3. Dependências de produção (as demais virão nas partes seguintes):
$ uv add django

# 4. Dependências de desenvolvimento:
$ uv add --dev pytest pytest-django ruff

# 5. Teste o ambiente:
$ uv run python -c "import django; print(django.get_version())"
```

## 📜 Exemplo de referência

### `pyproject.toml`

```toml
[project]
name = "ghanor-codex"
version = "0.1.0"
description = "Gerenciador de fichas e campanhas para A Lenda de Ghanor RPG"
requires-python = ">=3.12"
dependencies = [
    "django>=5.0",
]

[dependency-groups]
dev = [
    "pytest>=8.0",
    "pytest-django>=4.8",
    "ruff>=0.4",
]

[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "ghanor_codex.settings"
pythonpath = ["src"]
testpaths = ["tests"]

[tool.ruff]
line-length = 100
src = ["src", "tests"]

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]  # erros, imports, modernização, bugs comuns
```

### CI mínima — `.github/workflows/ci.yml`

```yaml
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv sync
      - run: uv run ruff check .
      - run: uv run pytest
```

## ⚔️ Exercícios

1. Configure o ambiente e faça o commit `chore: configura uv, pytest e ruff`.
2. Escreva um teste trivial em `tests/test_sanidade.py` (`def test_sanidade(): assert 1 + 1 == 2`) e confirme que `uv run pytest` passa — e que a CI passa no GitHub.
3. Rode `uv run ruff check .` e `uv run ruff format .` — deixe o hábito instalado desde já.

---

# PARTE 3 — Django: o esqueleto do projeto

## 🧠 Conceitos

### O que o Django é (e por que ele, revisitado)

Django é um framework *batteries included*: ORM, sistema de autenticação, painel administrativo, migrations, formulários, proteção contra as vulnerabilidades web clássicas (CSRF, SQL injection, XSS) — tudo incluso e integrado. Para os seus objetivos de aprendizado, cada "bateria" é um capítulo: você vai aprender ORM *usando* o ORM do Django, migrations *usando* as migrations dele, e assim por diante. (O racional completo contra FastAPI e Flask está no ADR-001.)

### MTV: a arquitetura do Django

Django usa o padrão **Model-Template-View** (uma variação do MVC):

- **Model** — classes Python que representam tabelas do banco. Onde os *dados* vivem.
- **View** — funções/classes que recebem uma requisição HTTP e devolvem uma resposta. Onde o *fluxo* vive.
- **Template** — HTML com marcações dinâmicas. Onde a *apresentação* vive.

```
Navegador ──HTTP──▶ urls.py ──▶ View ──▶ Model ──▶ PostgreSQL
                                  │
                                  ▼
                              Template ──HTML──▶ Navegador
```

### Projeto vs. Apps: a modularização do Django

Um **projeto** Django contém vários **apps** — módulos coesos e (idealmente) independentes. A regra de ouro: *um app deve fazer uma coisa e fazê-la bem*. Para o Ghanor Codex:

| App | Responsabilidade |
|---|---|
| `regras` | O catálogo do sistema: raças, classes, origens, perícias, poderes, magias. **Dados de referência**, quase imutáveis. |
| `fichas` | Personagens dos jogadores: criação (wizard), estado em sessão (PV/PM/inventário), evolução. **Dados vivos.** |
| `campanhas` | Mesas, sessões, vínculo mestre-jogadores. |

Essa separação segue o critério de **taxa de mudança**: dados de referência (o livro de regras) mudam quando sai errata; fichas mudam a cada sessão. Coisas que mudam por razões diferentes pertencem a módulos diferentes — esse é o *Single Responsibility Principle* aplicado a arquitetura, não só a classes.

### A camada de domínio: OOP de verdade

Aqui está a decisão mais importante da apostila: **as regras do jogo não vivem nos models do Django**. Elas vivem em módulos Python puros, em `dominio/`, sem nenhum import de Django.

Por quê?

1. **Testabilidade** — código puro testa sem banco, sem fixtures, em milissegundos.
2. **OOP de verdade** — você pratica classes, invariantes, polimorfismo e máquinas de estado sem o "ruído" do framework.
3. **Portabilidade** — se um dia migrar para FastAPI (Apêndice E), o domínio vai junto, intacto.

Este é o padrão que os livros chamam de *arquitetura hexagonal* ou *ports and adapters*, na sua forma mais simples: **o domínio no centro, o framework na borda**.

```
src/ghanor_codex/
├── settings.py, urls.py, wsgi.py     # configuração do projeto
├── dominio/                          # ⚠️ PYTHON PURO — as regras do jogo
│   ├── atributos.py
│   ├── criacao_ficha.py              # a máquina de estados (Parte 4)
│   └── progressao.py
├── regras/                           # app Django: catálogo
│   ├── models.py, admin.py, views.py ...
├── fichas/                           # app Django: personagens
└── campanhas/                        # app Django: mesas
```

## 🔨 Como montar

```bash
# 1. Crie o projeto Django DENTRO de src/ (o "." evita pasta duplicada):
$ cd src
$ uv run django-admin startproject ghanor_codex .
$ cd ..

# 2. Crie os apps:
$ cd src
$ uv run django-admin startapp regras
$ uv run django-admin startapp fichas
$ uv run django-admin startapp campanhas
$ mkdir ghanor_codex/dominio && touch ghanor_codex/dominio/__init__.py
$ cd ..

# 3. Registre os apps em settings.py (INSTALLED_APPS):
#    "regras", "fichas", "campanhas"

# 4. Suba e veja o foguete do Django:
$ uv run src/manage.py runserver
```

## 📜 Exemplo de referência

### `settings.py` — trechos essenciais (configuração via ambiente)

```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# NUNCA hardcode segredos: leia do ambiente (.env)
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
DEBUG = os.environ.get("DJANGO_DEBUG", "false").lower() == "true"
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # apps do Ghanor Codex
    "regras",
    "fichas",
    "campanhas",
]

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
```

> 💡 Para carregar o `.env` em desenvolvimento: `uv add django-environ` e siga a documentação — ou exporte as variáveis no shell. Em Docker (Parte 10), o Compose injeta o `.env` automaticamente.

## ⚔️ Exercícios

1. Suba o servidor e acesse `http://localhost:8000` — o foguete decolando confirma o setup.
2. Crie uma view "olá, aventureiro" em `fichas/views.py`, roteie em `urls.py` e escreva um teste com o client do pytest-django verificando o status 200. **Teste primeiro.**
3. Explique (para si, por escrito, no seu diário de aprendizado) por que `dominio/` não pode importar nada de `django.*`. Se a resposta sair fácil, a Parte 3 cumpriu a missão.

---

# PARTE 4 — O Domínio: regras do Tormenta 20 como código puro

## 🧠 Conceitos

Esta é a parte mais rica em OOP de toda a apostila — e ela não tem *nada* de Django.

### Modelando atributos

Tormenta 20 usa seis atributos (Força, Destreza, Constituição, Inteligência, Sabedoria, Carisma). Na criação, o jogador distribui valores; raça e outras escolhas aplicam modificadores. Conceitos de OOP em ação:

- **Value Object** — um conjunto de atributos é um valor imutável: modificar atributos *cria um novo* conjunto, não altera o existente. Imutabilidade elimina uma classe inteira de bugs ("quem mexeu no meu Carisma?"). Em Python: `@dataclass(frozen=True)`.
- **Invariantes** — regras que o objeto garante *sempre*: valores dentro da faixa permitida, os seis atributos presentes. O construtor valida; depois disso, o objeto é confiável por construção.

### A máquina de estados `FichaEmCriacao`

A criação de personagem em Tormenta 20 segue **8 passos ordenados**: atributos → raça → classe → origem → perícias → poderes → magias → toques finais. Cada passo depende dos anteriores (você não escolhe perícias antes da classe, porque a classe define quantas perícias você tem).

Isso é, formalmente, uma **máquina de estados finitos**: estados (os passos), transições permitidas (avançar após validar), e dados acumulados ao longo do caminho. Modelar isso explicitamente — em vez de espalhar `if`s por views — te dá:

- Um **único lugar** onde a sequência é imposta;
- **Validação de dependências** entre passos como método de cada passo;
- Facilidade de **serializar** o progresso (guardar a criação pela metade no banco, como JSONB — Parte 5).

### Efeitos de escolhas: o padrão que faz "elfo → +2 Carisma"

O requisito central do projeto: escolher uma opção altera a ficha. A modelagem elegante é tratar cada escolha como portadora de **efeitos** — pequenos objetos que sabem se aplicar a uma ficha:

```
Raça "Elfo" ──tem──▶ [ModificadorDeAtributo(CAR, +2),
                      ModificadorDeAtributo(INT, +1), ...]
```

Isso é o padrão **Strategy/Command** na prática: em vez de um `if raca == "elfo"` gigante, cada efeito é polimórfico — a ficha aplica a lista sem saber o que tem dentro. Adicionar uma raça nova = adicionar dados, não código. (E "dados, não código" é exatamente o que permitirá carregar raças do banco na Parte 5.)

## 🔨 Como montar

A ordem TDD para esta parte:

1. `tests/dominio/test_atributos.py` → implemente `dominio/atributos.py`
2. `tests/dominio/test_efeitos.py` → implemente `dominio/efeitos.py`
3. `tests/dominio/test_criacao_ficha.py` → implemente `dominio/criacao_ficha.py`

Rode `uv run pytest tests/dominio -v` obsessivamente. Sem banco, os testes rodam em milissegundos — aproveite o ciclo curto.

## 📜 Exemplo de referência

### `src/ghanor_codex/dominio/atributos.py`

```python
"""Atributos de personagem — Value Object imutável."""
from __future__ import annotations

from dataclasses import dataclass, replace
from enum import StrEnum


class Atributo(StrEnum):
    FORCA = "FOR"
    DESTREZA = "DES"
    CONSTITUICAO = "CON"
    INTELIGENCIA = "INT"
    SABEDORIA = "SAB"
    CARISMA = "CAR"


VALOR_MINIMO, VALOR_MAXIMO = -5, 20


@dataclass(frozen=True)
class ConjuntoDeAtributos:
    """Os seis atributos de um personagem.

    Imutável: aplicar um modificador devolve um NOVO conjunto.
    """

    valores: dict[Atributo, int]

    def __post_init__(self) -> None:
        faltando = set(Atributo) - set(self.valores)
        if faltando:
            raise ValueError(f"Atributos ausentes: {sorted(a.value for a in faltando)}")
        for atributo, valor in self.valores.items():
            if not (VALOR_MINIMO <= valor <= VALOR_MAXIMO):
                raise ValueError(
                    f"{atributo.value}={valor} fora da faixa [{VALOR_MINIMO}, {VALOR_MAXIMO}]"
                )

    def valor(self, atributo: Atributo) -> int:
        return self.valores[atributo]

    def com_modificador(self, atributo: Atributo, delta: int) -> "ConjuntoDeAtributos":
        """Devolve um novo conjunto com o modificador aplicado."""
        novos = {**self.valores, atributo: self.valores[atributo] + delta}
        return replace(self, valores=novos)
```

### `src/ghanor_codex/dominio/efeitos.py`

```python
"""Efeitos de escolhas de criação (raça, classe, origem...) sobre a ficha."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from ghanor_codex.dominio.atributos import Atributo, ConjuntoDeAtributos


class Efeito(Protocol):
    """Qualquer coisa que saiba se aplicar a um conjunto de atributos."""

    def aplicar(self, atributos: ConjuntoDeAtributos) -> ConjuntoDeAtributos: ...


@dataclass(frozen=True)
class ModificadorDeAtributo:
    """Ex.: elfo → ModificadorDeAtributo(Atributo.CARISMA, +2)."""

    atributo: Atributo
    delta: int

    def aplicar(self, atributos: ConjuntoDeAtributos) -> ConjuntoDeAtributos:
        return atributos.com_modificador(self.atributo, self.delta)


def aplicar_todos(
    atributos: ConjuntoDeAtributos, efeitos: list[Efeito]
) -> ConjuntoDeAtributos:
    for efeito in efeitos:
        atributos = efeito.aplicar(atributos)
    return atributos
```

### `src/ghanor_codex/dominio/criacao_ficha.py` (esqueleto da máquina de estados)

```python
"""Máquina de estados da criação de personagem — os 8 passos do Tormenta 20."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum, auto

from ghanor_codex.dominio.atributos import ConjuntoDeAtributos
from ghanor_codex.dominio.efeitos import Efeito, aplicar_todos


class Passo(StrEnum):
    ATRIBUTOS = auto()
    RACA = auto()
    CLASSE = auto()
    ORIGEM = auto()
    PERICIAS = auto()
    PODERES = auto()
    MAGIAS = auto()
    TOQUES_FINAIS = auto()


ORDEM_DOS_PASSOS: list[Passo] = list(Passo)


class PassoForaDeOrdem(Exception):
    pass


@dataclass
class FichaEmCriacao:
    """Acumula as escolhas do jogador, impondo a ordem dos passos."""

    atributos_base: ConjuntoDeAtributos | None = None
    escolhas: dict[Passo, str] = field(default_factory=dict)
    efeitos_acumulados: list[Efeito] = field(default_factory=list)
    _indice_passo: int = 0

    @property
    def passo_atual(self) -> Passo:
        return ORDEM_DOS_PASSOS[self._indice_passo]

    def _exigir_passo(self, passo: Passo) -> None:
        if passo != self.passo_atual:
            raise PassoForaDeOrdem(
                f"Passo atual é {self.passo_atual.name}, tentou {passo.name}"
            )

    def definir_atributos(self, atributos: ConjuntoDeAtributos) -> None:
        self._exigir_passo(Passo.ATRIBUTOS)
        self.atributos_base = atributos
        self._avancar()

    def escolher_raca(self, nome: str, efeitos: list[Efeito]) -> None:
        self._exigir_passo(Passo.RACA)
        self.escolhas[Passo.RACA] = nome
        self.efeitos_acumulados.extend(efeitos)
        self._avancar()

    # ... escolher_classe, escolher_origem etc. seguem o mesmo padrão ...

    def _avancar(self) -> None:
        self._indice_passo += 1

    @property
    def atributos_finais(self) -> ConjuntoDeAtributos:
        if self.atributos_base is None:
            raise ValueError("Atributos base ainda não definidos")
        return aplicar_todos(self.atributos_base, self.efeitos_acumulados)
```

### `tests/dominio/test_criacao_ficha.py` (o teste que veio ANTES)

```python
import pytest

from ghanor_codex.dominio.atributos import Atributo, ConjuntoDeAtributos
from ghanor_codex.dominio.criacao_ficha import FichaEmCriacao, PassoForaDeOrdem
from ghanor_codex.dominio.efeitos import ModificadorDeAtributo


def atributos_padrao() -> ConjuntoDeAtributos:
    return ConjuntoDeAtributos(valores={a: 1 for a in Atributo})


def test_elfo_recebe_mais_dois_de_carisma() -> None:
    ficha = FichaEmCriacao()
    ficha.definir_atributos(atributos_padrao())

    ficha.escolher_raca("Elfo", efeitos=[ModificadorDeAtributo(Atributo.CARISMA, +2)])

    assert ficha.atributos_finais.valor(Atributo.CARISMA) == 3


def test_nao_pode_escolher_raca_antes_dos_atributos() -> None:
    ficha = FichaEmCriacao()

    with pytest.raises(PassoForaDeOrdem):
        ficha.escolher_raca("Elfo", efeitos=[])
```

## ⚔️ Exercícios

1. **TDD:** implemente `escolher_classe`, que além dos efeitos define PV e PM iniciais (consulte o livro no Drive para os valores por classe).
2. **TDD:** um humano recebe +1 em três atributos *à escolha* — modele isso (dica: o efeito pode ser parametrizado na hora da escolha).
3. Adicione o método `para_dict()` / `de_dict()` na `FichaEmCriacao` — serialização que a Parte 5 vai usar para persistir o progresso em JSONB.
4. Rode `uv run pytest tests/dominio --durations=5` e observe: testes de domínio puro em milissegundos. *Esse* é o dividendo da arquitetura.

---

# PARTE 5 — Banco de Dados: PostgreSQL, Models e a decisão JSONB

## 🧠 Conceitos

### Relacional vs. semiestruturado: a tensão central dos dados de RPG

Parte dos dados do Ghanor Codex é perfeitamente relacional: um personagem *pertence a* um usuário, *participa de* uma campanha, *tem uma* raça. Chaves estrangeiras, integridade referencial — o feijão com arroz relacional.

Mas a **ficha em si** é rebelde: um guerreiro tem manobras, um arcanista tem grimório com slots, cada poder tem campos diferentes. Modelar cada variação como tabela geraria dezenas de tabelas quase vazias e JOINs infernais.

A resposta (ADR-001): **JSONB do PostgreSQL**. Colunas que armazenam JSON binário, indexável e consultável. Você obtém a flexibilidade de documento *dentro* do banco relacional, com transações ACID e um único sistema para operar.

**A regra de decisão para cada campo:**

> Se você precisa fazer JOIN, filtrar em lista ou garantir integridade referencial → **coluna/tabela relacional**.
> Se é um "saco de propriedades" que só a ficha usa e cuja estrutura varia → **JSONB**.

### Migrations: o versionamento do banco

Cada mudança nos models gera uma **migration** — um script Python que descreve a alteração do esquema. Migrations são versionadas no Git, aplicadas em ordem, e permitem que qualquer ambiente (seu notebook, o home lab, a CI) reconstrua o banco idêntico. É o Git do esquema.

### Índices: GIN para JSONB

Consultas em colunas JSONB (`dados__pv__lte=10`) sem índice fazem varredura completa da tabela. O índice **GIN** (Generalized Inverted Index) indexa as chaves e valores internos do JSON, tornando essas consultas rápidas. Você vai declará-lo direto no model.

## 🔨 Como montar

```bash
# 1. Suba o PostgreSQL via Docker (o compose completo vem na Parte 10;
#    por ora, um serviço só):
$ docker compose up -d db

# 2. Adicione o driver:
$ uv add "psycopg[binary]"

# 3. Aponte o settings.py para o Postgres (exemplo abaixo)

# 4. Modele em regras/models.py e fichas/models.py

# 5. Gere e aplique as migrations:
$ uv run src/manage.py makemigrations
$ uv run src/manage.py migrate
```

### `compose.yaml` (versão mínima desta parte)

```yaml
services:
  db:
    image: postgres:16
    env_file: .env
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

### `settings.py` — banco

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["POSTGRES_DB"],
        "USER": os.environ["POSTGRES_USER"],
        "PASSWORD": os.environ["POSTGRES_PASSWORD"],
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}
```

## 📜 Exemplo de referência

### `src/regras/models.py` — o catálogo (dados de referência)

```python
from django.db import models


class Raca(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    descricao = models.TextField(blank=True)
    # Efeitos como dados (Parte 4!): [{"tipo": "mod_atributo", "atributo": "CAR", "delta": 2}]
    efeitos = models.JSONField(default=list)

    class Meta:
        verbose_name_plural = "raças"

    def __str__(self) -> str:
        return self.nome


class Classe(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    pv_inicial = models.PositiveSmallIntegerField()
    pv_por_nivel = models.PositiveSmallIntegerField()
    pm_por_nivel = models.PositiveSmallIntegerField()
    pericias_quantidade = models.PositiveSmallIntegerField()
    efeitos = models.JSONField(default=list)

    def __str__(self) -> str:
        return self.nome


class Magia(models.Model):
    class Circulo(models.IntegerChoices):
        PRIMEIRO = 1
        SEGUNDO = 2
        TERCEIRO = 3
        QUARTO = 4
        QUINTO = 5

    nome = models.CharField(max_length=100, unique=True)
    circulo = models.IntegerField(choices=Circulo.choices)
    escola = models.CharField(max_length=30)
    custo_pm = models.PositiveSmallIntegerField()
    # Campos que variam muito por magia: alcance, duração, resistência, aprimoramentos...
    detalhes = models.JSONField(default=dict)
    descricao = models.TextField()

    class Meta:
        indexes = [
            models.Index(fields=["circulo", "escola"]),
        ]

    def __str__(self) -> str:
        return f"{self.nome} ({self.circulo}º círculo)"
```

### `src/fichas/models.py` — dados vivos, com JSONB e GIN

```python
from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from django.db import models

from regras.models import Classe, Magia, Raca


class Personagem(models.Model):
    class Status(models.TextChoices):
        EM_CRIACAO = "em_criacao", "Em criação"
        ATIVO = "ativo", "Ativo"
        APOSENTADO = "aposentado", "Aposentado"

    # Relacional: precisa de JOIN e integridade → colunas normais
    jogador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    raca = models.ForeignKey(Raca, null=True, on_delete=models.PROTECT)
    classe = models.ForeignKey(Classe, null=True, on_delete=models.PROTECT)
    magias = models.ManyToManyField(Magia, blank=True)
    nivel = models.PositiveSmallIntegerField(default=1)
    status = models.CharField(max_length=20, choices=Status.choices,
                              default=Status.EM_CRIACAO)

    # Semiestruturado: o "corpo" da ficha → JSONB
    # {"atributos": {"FOR": 2, ...}, "pv": {"atual": 18, "max": 20},
    #  "pm": {"atual": 4, "max": 6}, "inventario": [...], "pericias": [...]}
    dados = models.JSONField(default=dict)

    # Progresso do wizard (serialização da FichaEmCriacao da Parte 4)
    criacao = models.JSONField(default=dict)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [GinIndex(fields=["dados"])]
        verbose_name_plural = "personagens"

    def __str__(self) -> str:
        return f"{self.nome} ({self.jogador})"
```

### Consultando JSONB pelo ORM

```python
# Personagens com PV atual abaixo de 10 (o GIN faz isso voar):
feridos = Personagem.objects.filter(dados__pv__atual__lt=10)

# Quem tem "Corda de seda" no inventário:
com_corda = Personagem.objects.filter(dados__inventario__contains=[{"item": "Corda de seda"}])
```

## ⚔️ Exercícios

1. **TDD (com `pytest.mark.django_db`):** teste que criar um `Personagem` com `dados` vazio e depois atualizar `dados["pv"]` persiste corretamente.
2. Modele `Origem`, `Pericia` e `Poder` em `regras/models.py`, decidindo campo a campo: relacional ou JSONB? Justifique num comentário — essa justificativa é o aprendizado.
3. Escreva `scripts/seed_regras.py` que carrega 3 raças e 2 classes com seus efeitos (extraia os valores do livro no Drive). Rode com `uv run src/manage.py shell < scripts/seed_regras.py` ou converta num *management command* (pesquise `BaseCommand` — vale o desvio).
4. No `psql` (`docker compose exec db psql -U ghanor`), rode `EXPLAIN ANALYZE` numa consulta JSONB com e sem o índice GIN. Ver o plano de execução mudar é aprender índices de verdade.

---

# PARTE 6 — Django Admin: o painel do Mestre "de graça"

## 🧠 Conceitos

O **Django Admin** gera uma interface CRUD completa a partir dos seus models: listagem com busca e filtros, formulários com validação, controle de permissões. Para o Ghanor Codex ele tem dois papéis:

1. **Ferramenta de carga do catálogo** — cadastrar raças, classes, magias do livro sem escrever telas.
2. **Painel do Mestre (MVP)** — o mestre da mesa consulta e ajusta fichas por ali enquanto as telas bonitas não existem.

A lição de engenharia: **não construa o que você ganha de graça**. Todo o esforço de tela que o Admin economiza vai para o que é único do seu projeto (o wizard, a tela de sessão).

## 🔨 Como montar

```bash
$ uv run src/manage.py createsuperuser
$ uv run src/manage.py runserver
# acesse http://localhost:8000/admin
```

## 📜 Exemplo de referência

### `src/regras/admin.py`

```python
from django.contrib import admin

from regras.models import Classe, Magia, Raca


@admin.register(Raca)
class RacaAdmin(admin.ModelAdmin):
    list_display = ("nome",)
    search_fields = ("nome",)


@admin.register(Magia)
class MagiaAdmin(admin.ModelAdmin):
    list_display = ("nome", "circulo", "escola", "custo_pm")
    list_filter = ("circulo", "escola")
    search_fields = ("nome", "descricao")


@admin.register(Classe)
class ClasseAdmin(admin.ModelAdmin):
    list_display = ("nome", "pv_inicial", "pv_por_nivel", "pm_por_nivel")
```

## ⚔️ Exercícios

1. Registre `Personagem` no admin com `list_display` mostrando nome, jogador, nível e status, e `list_filter` por status.
2. Cadastre pelo Admin 5 magias de 1º círculo do livro (Drive) — você vai usá-las nas Partes 7 e 8.
3. Pesquise `readonly_fields` e proteja `criado_em`/`atualizado_em` de edição.

---

# PARTE 7 — API REST com Django REST Framework

## 🧠 Conceitos

### O que é uma API REST, na prática

Uma API expõe seus dados por HTTP em formato neutro (JSON), permitindo que *qualquer* cliente consuma: o frontend HTMX, um futuro app mobile, a trilha React do Apêndice E, um bot de Discord da sua mesa. REST organiza isso em **recursos** (substantivos, não verbos) manipulados pelos verbos HTTP:

| Verbo + rota | Significado |
|---|---|
| `GET /api/v1/magias/` | listar magias |
| `GET /api/v1/magias/42/` | detalhar a magia 42 |
| `POST /api/v1/personagens/` | criar personagem |
| `PATCH /api/v1/personagens/7/` | atualizar parcialmente (ex.: PV) |
| `DELETE /api/v1/personagens/7/` | remover |

O `/v1/` na rota é **versionamento**: quando (não "se") o contrato mudar de forma incompatível, o `/v2/` nasce sem quebrar quem usa o `/v1/`.

### As três peças do DRF

- **Serializer** — traduz model ↔ JSON e valida entrada. É a *fronteira* do sistema: nada entra sem passar por ele.
- **ViewSet** — agrupa as operações CRUD de um recurso numa classe só.
- **Router** — gera as rotas REST convencionais a partir do ViewSet.

### Permissões: quem pode o quê

Regra do Ghanor Codex: qualquer autenticado **lê** o catálogo; só o **dono** edita a própria ficha; o mestre da campanha lê as fichas da mesa. Isso se expressa em classes de permissão — pequenas, testáveis, reutilizáveis.

## 🔨 Como montar

```bash
$ uv add djangorestframework
# adicione "rest_framework" em INSTALLED_APPS
```

## 📜 Exemplo de referência

### `src/regras/serializers.py`

```python
from rest_framework import serializers

from regras.models import Magia


class MagiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Magia
        fields = ["id", "nome", "circulo", "escola", "custo_pm", "detalhes", "descricao"]
```

### `src/regras/views.py`

```python
from rest_framework import viewsets

from regras.models import Magia
from regras.serializers import MagiaSerializer


class MagiaViewSet(viewsets.ReadOnlyModelViewSet):
    """Catálogo é somente leitura via API — quem edita é o Admin."""

    queryset = Magia.objects.all().order_by("circulo", "nome")
    serializer_class = MagiaSerializer
    filterset_fields = ["circulo", "escola"]
    search_fields = ["nome", "descricao"]
```

### `src/ghanor_codex/urls.py`

```python
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from regras.views import MagiaViewSet

router = DefaultRouter()
router.register("magias", MagiaViewSet, basename="magia")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(router.urls)),
]
```

### Permissão "só o dono" — `src/fichas/permissions.py`

```python
from rest_framework import permissions


class ApenasDono(permissions.BasePermission):
    """Escrita permitida apenas ao jogador dono do personagem."""

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.jogador == request.user
```

### Teste de API — `tests/api/test_magias.py`

```python
import pytest
from rest_framework.test import APIClient

from regras.models import Magia


@pytest.mark.django_db
def test_lista_magias_filtrando_por_circulo() -> None:
    Magia.objects.create(nome="Luz", circulo=1, escola="Evocação", custo_pm=1,
                         descricao="Cria luz.")
    Magia.objects.create(nome="Bola de Fogo", circulo=3, escola="Evocação",
                         custo_pm=6, descricao="BOOM.")
    client = APIClient()

    resposta = client.get("/api/v1/magias/", {"circulo": 1})

    assert resposta.status_code == 200
    nomes = [m["nome"] for m in resposta.json()["results"]]
    assert nomes == ["Luz"]
```

## ⚔️ Exercícios

1. **TDD:** crie o `PersonagemViewSet` com a permissão `ApenasDono` — o teste deve provar que o usuário B recebe **403** ao tentar `PATCH` na ficha do usuário A.
2. Adicione paginação global no DRF (`PAGE_SIZE = 20`) e busca (`?search=fogo`) nas magias (`uv add django-filter`).
3. Explore a API navegável do DRF no navegador (`/api/v1/magias/`) — ela é a documentação viva do seu contrato.
4. **Desafio:** endpoint de ação customizada `POST /api/v1/personagens/{id}/dano/` com corpo `{"quantidade": 5}` que reduz o PV via lógica do **domínio** (a view não faz conta — ela delega).

---

# PARTE 8 — Frontend: HTMX + Alpine.js + Tailwind

## 🧠 Conceitos

### A filosofia: hipermídia em vez de SPA

O modelo HTMX inverte a lógica das SPAs: em vez de o servidor mandar JSON para um JavaScript gigante montar HTML no cliente, **o servidor manda o próprio HTML** — e o HTMX troca pedaços da página. Atributos no HTML declaram o comportamento:

```html
<button hx-post="/fichas/7/dano/"
        hx-vals='{"quantidade": 1}'
        hx-target="#pv-display"
        hx-swap="outerHTML">
  Sofrer 1 de dano
</button>
```

Traduzindo: "ao clicar, faça POST nessa URL e substitua o elemento `#pv-display` pelo HTML que voltar". Sem JavaScript escrito por você. A view Django devolve um **parcial** — um template pequeno com só o pedaço atualizado.

**Divisão de trabalho do trio:**

- **HTMX** — tudo que conversa com o servidor (salvar, buscar, navegar entre passos do wizard).
- **Alpine.js** — micro-interatividade que *não* precisa do servidor (abrir/fechar modal, tabs, contador visual).
- **Tailwind** — estilo utilitário direto no HTML; produtividade sem escrever CSS do zero.

### Templates: herança e parciais

O sistema de templates do Django tem duas ferramentas-chave:

- **Herança** — `base.html` define o layout (menu, fontes, HTMX/Alpine carregados); cada página o estende e preenche blocos.
- **Parciais** — templates fragmento (convenção: prefixo `_`, ex.: `_pv_display.html`) usados tanto na renderização inicial (`{% include %}`) quanto como resposta HTMX. **Um parcial, duas serventias** — esse é o truque que mantém tudo DRY.

### A consulta rápida de magias (requisito de ouro do projeto)

O jogador está na tela da ficha e quer saber o que "Bola de Fogo" faz *agora*. Padrão: busca com `hx-trigger="keyup changed delay:300ms"` (dispara 300ms após parar de digitar — isso se chama *debounce*) que devolve um parcial com os resultados. Servidor busca no JSONB indexado; resposta em milissegundos.

## 🔨 Como montar

```bash
# HTMX e Alpine entram por CDN no base.html (simples e suficiente).
# Tailwind: para o MVP, use o CDN também; a build otimizada fica para o deploy.
$ mkdir -p src/templates src/fichas/templates/fichas
# settings.py → TEMPLATES[0]["DIRS"] = [BASE_DIR / "templates"]
```

## 📜 Exemplo de referência

### `src/templates/base.html`

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{% block titulo %}Ghanor Codex{% endblock %}</title>
  <script src="https://unpkg.com/htmx.org@2.0.4"></script>
  <script defer src="https://unpkg.com/alpinejs@3.14.3/dist/cdn.min.js"></script>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-stone-900 text-stone-100 min-h-screen"
      hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'>
  <nav class="p-4 border-b border-stone-700">
    <a href="/" class="font-bold text-amber-400">⚔️ Ghanor Codex</a>
  </nav>
  <main class="max-w-4xl mx-auto p-4">
    {% block conteudo %}{% endblock %}
  </main>
</body>
</html>
```

### Busca de magias — `src/fichas/templates/fichas/detalhe.html` (trecho)

```html
{% extends "base.html" %}
{% block conteudo %}
  <h1 class="text-2xl font-bold">{{ personagem.nome }}</h1>

  {% include "fichas/_pv_display.html" %}

  <section class="mt-6">
    <h2 class="text-lg text-amber-400">Consultar magias</h2>
    <input type="search" name="q"
           placeholder="Digite o nome da magia..."
           class="w-full p-2 rounded bg-stone-800 border border-stone-600"
           hx-get="{% url 'fichas:buscar_magias' personagem.id %}"
           hx-trigger="keyup changed delay:300ms"
           hx-target="#resultados-magias">
    <div id="resultados-magias" class="mt-2"></div>
  </section>
{% endblock %}
```

### Parcial de resultados — `_resultados_magias.html`

```html
{% for magia in magias %}
  <div class="p-3 mb-2 rounded bg-stone-800" x-data="{ aberto: false }">
    <button @click="aberto = !aberto" class="w-full text-left font-semibold">
      {{ magia.nome }}
      <span class="text-stone-400 text-sm">
        — {{ magia.get_circulo_display }} círculo · {{ magia.custo_pm }} PM
      </span>
    </button>
    <p x-show="aberto" x-cloak class="mt-2 text-sm text-stone-300">
      {{ magia.descricao }}
    </p>
  </div>
{% empty %}
  <p class="text-stone-500">Nenhuma magia encontrada.</p>
{% endfor %}
```

### View da busca — `src/fichas/views.py` (trecho)

```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from fichas.models import Personagem


@login_required
def buscar_magias(request, personagem_id: int):
    personagem = get_object_or_404(Personagem, id=personagem_id,
                                   jogador=request.user)
    consulta = request.GET.get("q", "").strip()
    magias = personagem.magias.filter(nome__icontains=consulta) if consulta else []
    return render(request, "fichas/_resultados_magias.html", {"magias": magias})
```

### PV com HTMX — parcial `_pv_display.html` + view

```html
<div id="pv-display" class="flex items-center gap-3 mt-4">
  <span class="text-xl">❤️ {{ personagem.dados.pv.atual }}/{{ personagem.dados.pv.max }}</span>
  <button class="px-3 py-1 rounded bg-red-800"
          hx-post="{% url 'fichas:aplicar_dano' personagem.id %}"
          hx-vals='{"quantidade": 1}'
          hx-target="#pv-display" hx-swap="outerHTML">−1</button>
  <button class="px-3 py-1 rounded bg-green-800"
          hx-post="{% url 'fichas:curar' personagem.id %}"
          hx-vals='{"quantidade": 1}'
          hx-target="#pv-display" hx-swap="outerHTML">+1</button>
</div>
```

```python
@login_required
def aplicar_dano(request, personagem_id: int):
    personagem = get_object_or_404(Personagem, id=personagem_id,
                                   jogador=request.user)
    quantidade = int(request.POST["quantidade"])
    pv = personagem.dados["pv"]
    pv["atual"] = max(0, pv["atual"] - quantidade)   # regra simples aqui;
    personagem.save(update_fields=["dados", "atualizado_em"])  # regras complexas → dominio/
    return render(request, "fichas/_pv_display.html", {"personagem": personagem})
```

## ⚔️ Exercícios

1. Implemente a view `curar` (espelho do dano, sem passar do máximo) — **teste primeiro**, incluindo o caso de borda "curar acima do máximo".
2. Faça a busca de magias também filtrar pela descrição (encontrar "fogo" deve achar Bola de Fogo mesmo que o nome pesquisado seja parte da descrição).
3. Com Alpine, adicione um "modo de rolagem": um botão que mostra/esconde um painel com o modificador de cada atributo da ficha.
4. Abra as ferramentas de rede do navegador e observe as respostas HTMX: são HTML, não JSON. Internalizar isso é internalizar o paradigma.

---

# PARTE 9 — O Wizard de Criação: onde tudo se encontra

## 🧠 Conceitos

Esta parte não introduz tecnologia nova — ela **integra** tudo: a máquina de estados (Parte 4), a persistência do progresso em JSONB (Parte 5), o catálogo (Partes 5–6) e os parciais HTMX (Parte 8).

### O fluxo por requisição

```
1. GET /fichas/criar/            → cria Personagem(status=EM_CRIACAO), redireciona
2. GET /fichas/7/wizard/         → carrega FichaEmCriacao do campo `criacao` (JSONB)
                                    e renderiza o parcial do passo atual
3. POST do passo (via HTMX)      → reconstrói FichaEmCriacao ← JSONB
                                    aplica a escolha (o DOMÍNIO valida ordem e regras)
                                    serializa de volta → JSONB, salva
                                    devolve o parcial do PRÓXIMO passo
4. Último passo concluído        → materializa `dados` finais, status=ATIVO
```

Repare no padrão **carregar → operar no domínio → persistir**: a view é só um *adaptador* entre HTTP e o domínio. Se um POST tentar pular um passo, quem barra é a `PassoForaDeOrdem` do domínio — a view apenas traduz a exceção em resposta HTTP amigável. **A regra vive num lugar só.**

### Por que essa separação brilha aqui

Sem a máquina de estados, o wizard viraria uma teia de `if`s espalhados por 8 views — o tipo de código que apodrece. Com ela, cada view do wizard tem ~10 linhas e o comportamento inteiro está coberto pelos testes de domínio que você já escreveu na Parte 4. Este é o momento "aha" da arquitetura.

## 🔨 Como montar

1. Adicione `para_dict()`/`de_dict()` na `FichaEmCriacao` (exercício da Parte 4 — agora ele paga).
2. Crie um parcial por passo: `_passo_atributos.html`, `_passo_raca.html`, ...
3. Uma view genérica `wizard_passo` roteia o POST para o método certo do domínio.
4. Um serviço `materializar_ficha(ficha_em_criacao) -> dict` monta o campo `dados` final.

## 📜 Exemplo de referência

### `src/fichas/views.py` — o passo de raça (padrão para os demais)

```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from fichas.models import Personagem
from ghanor_codex.dominio.criacao_ficha import FichaEmCriacao, PassoForaDeOrdem
from ghanor_codex.dominio.efeitos import ModificadorDeAtributo
from ghanor_codex.dominio.atributos import Atributo
from regras.models import Raca


def _efeitos_da_raca(raca: Raca) -> list:
    """Traduz efeitos-como-dados (JSONB do catálogo) em objetos do domínio."""
    efeitos = []
    for e in raca.efeitos:
        if e["tipo"] == "mod_atributo":
            efeitos.append(ModificadorDeAtributo(Atributo(e["atributo"]), e["delta"]))
    return efeitos


@login_required
def wizard_escolher_raca(request, personagem_id: int):
    personagem = get_object_or_404(
        Personagem, id=personagem_id, jogador=request.user,
        status=Personagem.Status.EM_CRIACAO,
    )
    ficha = FichaEmCriacao.de_dict(personagem.criacao)

    if request.method == "POST":
        raca = get_object_or_404(Raca, id=request.POST["raca_id"])
        try:
            ficha.escolher_raca(raca.nome, efeitos=_efeitos_da_raca(raca))
        except PassoForaDeOrdem:
            return render(request, "fichas/_erro_wizard.html",
                          {"mensagem": "Complete o passo anterior primeiro."},
                          status=409)
        personagem.raca = raca
        personagem.criacao = ficha.para_dict()
        personagem.save(update_fields=["raca", "criacao", "atualizado_em"])
        return render(request, "fichas/_passo_classe.html",
                      {"personagem": personagem, "ficha": ficha})

    return render(request, "fichas/_passo_raca.html",
                  {"personagem": personagem, "racas": Raca.objects.all()})
```

### `_passo_raca.html`

```html
<div id="wizard-passo">
  <h2 class="text-xl text-amber-400 mb-3">Passo 2 de 8 — Escolha sua raça</h2>
  <form hx-post="{% url 'fichas:wizard_raca' personagem.id %}"
        hx-target="#wizard-passo" hx-swap="outerHTML">
    {% for raca in racas %}
      <label class="block p-3 mb-2 rounded bg-stone-800 cursor-pointer
                    has-[:checked]:ring-2 has-[:checked]:ring-amber-400">
        <input type="radio" name="raca_id" value="{{ raca.id }}" class="mr-2" required>
        <span class="font-semibold">{{ raca.nome }}</span>
        <span class="text-sm text-stone-400 block">{{ raca.descricao|truncatewords:20 }}</span>
      </label>
    {% endfor %}
    <button class="mt-3 px-4 py-2 rounded bg-amber-600 font-semibold">
      Confirmar raça →
    </button>
  </form>
</div>
```

## ⚔️ Exercícios

1. Implemente os passos de classe e origem seguindo o padrão. Ao escolher a classe, PV/PM iniciais entram na `FichaEmCriacao`.
2. **TDD de integração:** um teste que percorre o wizard inteiro via client HTTP e verifica que o personagem final tem `status=ATIVO` e o Carisma correto para um elfo.
3. Adicione uma barra de progresso (passo N de 8) no topo de cada parcial — o número vem de `ficha.passo_atual`.
4. **Desafio:** botão "voltar um passo". Que métodos a máquina de estados precisa ganhar? Quais escolhas precisam ser *desfeitas* (efeitos removidos)? Escreva os testes de domínio primeiro — este exercício vale por três.

---

# PARTE 10 — Gestão de Sessão e Progressão

## 🧠 Conceitos

Com a ficha criada, entra o dia a dia da mesa: dano, cura, gasto de PM, itens entrando e saindo, condições (envenenado, caído...), e o momento glorioso de **subir de nível**.

### Regras de sessão pertencem ao domínio

"PV não passa do máximo", "PM insuficiente impede conjurar", "ao subir de nível, PV máximo aumenta conforme a classe" — tudo isso é regra de negócio. Crie `dominio/sessao.py` e `dominio/progressao.py`. As views (HTML e API) apenas delegam. Você já conhece o padrão; agora é praticar até virar reflexo.

### Concorrência: o mestre e o jogador mexem na mesma ficha

Se o mestre aplica dano no mesmo instante em que o jogador se cura, uma escrita pode sobrepor a outra (*lost update*). Solução: **transação com trava de linha**:

```python
from django.db import transaction

with transaction.atomic():
    personagem = Personagem.objects.select_for_update().get(id=pid)
    # ler → operar no domínio → salvar, tudo dentro da trava
```

O `select_for_update` faz o segundo acesso esperar o primeiro terminar. É a introdução perfeita a transações e isolamento — conceitos que valem para qualquer sistema que você construir na vida.

## 📜 Exemplo de referência

### `src/ghanor_codex/dominio/progressao.py`

```python
"""Regras de subida de nível."""
from dataclasses import dataclass


@dataclass(frozen=True)
class GanhosDeNivel:
    pv_maximo_extra: int
    pm_maximo_extra: int
    novo_nivel: int


def subir_de_nivel(nivel_atual: int, pv_por_nivel: int, pm_por_nivel: int,
                   mod_constituicao: int) -> GanhosDeNivel:
    """Tormenta 20: PV por nível = valor da classe + mod. de Constituição."""
    if nivel_atual >= 20:
        raise ValueError("Nível máximo (20) já alcançado")
    return GanhosDeNivel(
        pv_maximo_extra=pv_por_nivel + mod_constituicao,
        pm_maximo_extra=pm_por_nivel,
        novo_nivel=nivel_atual + 1,
    )
```

### Teste correspondente

```python
import pytest

from ghanor_codex.dominio.progressao import subir_de_nivel


def test_guerreiro_con_2_ganha_pv_da_classe_mais_constituicao() -> None:
    ganhos = subir_de_nivel(nivel_atual=1, pv_por_nivel=5, pm_por_nivel=3,
                            mod_constituicao=2)
    assert ganhos.pv_maximo_extra == 7
    assert ganhos.novo_nivel == 2


def test_nivel_20_nao_sobe_mais() -> None:
    with pytest.raises(ValueError):
        subir_de_nivel(20, 5, 3, 2)
```

## ⚔️ Exercícios

1. **TDD:** `dominio/sessao.py` com `aplicar_dano`, `curar` e `gastar_pm` — incluindo os casos de borda (PV a zero, PM insuficiente). Depois refatore as views da Parte 8 para delegar a ele.
2. Modele o inventário como lista em JSONB (`[{"item": "...", "quantidade": 2, "peso": 1.0}]`) com tela HTMX de adicionar/remover e o total de carga calculado no domínio.
3. Implemente condições (envenenado, atordoado...) como *badges* na ficha, com toggle HTMX.
4. **Desafio:** o fluxo completo de subir de nível — botão na ficha → view com `select_for_update` → domínio calcula ganhos → JSONB atualizado → parcial devolve a ficha renovada. Escreva um teste que simula duas escritas concorrentes.

---

# PARTE 11 — Campanhas e Permissões

## 🧠 Conceitos

O app `campanhas` conecta pessoas: um mestre, vários jogadores, sessões com data e anotações. Tecnicamente, é seu laboratório de **relacionamentos** (M2M com `through` para dados extras no vínculo) e de **autorização por papel**: o que o mestre pode (ver todas as fichas da mesa) difere do que o jogador pode (editar só a sua).

Autorização em duas camadas, sempre: nas **queries** (o jogador nem *vê* fichas de outras mesas — filtre o queryset) e nas **ações** (permissões DRF / verificações na view). Segurança em profundidade.

## 📜 Exemplo de referência

```python
# src/campanhas/models.py
from django.conf import settings
from django.db import models

from fichas.models import Personagem


class Campanha(models.Model):
    nome = models.CharField(max_length=100)
    mestre = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name="campanhas_mestradas")
    personagens = models.ManyToManyField(Personagem, blank=True,
                                         related_name="campanhas")
    descricao = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.nome


class Sessao(models.Model):
    campanha = models.ForeignKey(Campanha, on_delete=models.CASCADE,
                                 related_name="sessoes")
    numero = models.PositiveSmallIntegerField()
    data = models.DateField()
    resumo = models.TextField(blank=True)

    class Meta:
        unique_together = [("campanha", "numero")]
        verbose_name_plural = "sessões"
```

## ⚔️ Exercícios

1. **TDD:** o mestre lista todas as fichas da sua campanha; um jogador de outra mesa recebe queryset vazio (não 403 — ele nem sabe que existe).
2. Tela do mestre: todas as fichas da mesa com PV/PM visíveis, atualizando a cada 30s (`hx-trigger="every 30s"`) — seu primeiro *polling*.
3. Convite por link: token na URL adiciona o personagem do convidado à campanha. Pense no ciclo de vida do token (expira? single-use?) e documente a decisão num mini-ADR.

---

# PARTE 12 — Deploy: Docker Compose, Caddy e o Home Lab

## 🧠 Conceitos

### Dev ≠ Prod, e o que muda

Em produção: `DEBUG=false` (páginas de erro do Django vazam código), um servidor WSGI de verdade (**gunicorn** — o `runserver` é só para dev), arquivos estáticos servidos com eficiência (**whitenoise**), e HTTPS (**Caddy**, que obtém e renova certificados sozinho).

### A anatomia do Compose de produção

```
Internet ──443──▶ Caddy ──▶ web (gunicorn/Django) ──▶ db (PostgreSQL)
                                                  └──▶ metabase (read-only)
```

Cada serviço num container; a rede interna do Compose os conecta pelo *nome do serviço* (o Django acha o banco em `db:5432`). Volumes persistem o que não pode morrer com o container (dados do Postgres).

### Metabase e o usuário read-only

O Metabase se conecta com um usuário PostgreSQL **somente leitura** — princípio do menor privilégio: a ferramenta de dashboards não tem como corromper dados. Você cria esse usuário com duas linhas de SQL e ganha dashboards ("distribuição de classes", "PV médio por sessão") de graça.

## 📜 Exemplo de referência

### `Dockerfile`

```dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY src/ ./src/
RUN uv run src/manage.py collectstatic --noinput

EXPOSE 8000
CMD ["uv", "run", "gunicorn", "--chdir", "src",
     "--bind", "0.0.0.0:8000", "ghanor_codex.wsgi"]
```

### `compose.yaml` (produção)

```yaml
services:
  caddy:
    image: caddy:2
    ports: ["80:80", "443:443"]
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile:ro
      - caddy_data:/data
    depends_on: [web]

  web:
    build: .
    env_file: .env
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped

  db:
    image: postgres:16
    env_file: .env
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $$POSTGRES_USER"]
      interval: 5s
      retries: 5

  metabase:
    image: metabase/metabase:latest
    ports: ["3000:3000"]
    depends_on: [db]

volumes:
  pgdata:
  caddy_data:
```

### `Caddyfile`

```
ghanor.seudominio.com {
    reverse_proxy web:8000
}
```

### Usuário read-only para o Metabase

```sql
CREATE USER metabase_ro WITH PASSWORD 'senha-forte-aqui';
GRANT CONNECT ON DATABASE ghanor TO metabase_ro;
GRANT USAGE ON SCHEMA public TO metabase_ro;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO metabase_ro;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO metabase_ro;
```

## ⚔️ Exercícios

1. Suba a stack completa no home lab: `docker compose up -d --build`, rode as migrations dentro do container (`docker compose exec web uv run src/manage.py migrate`) e acesse pelo domínio com HTTPS.
2. Configure `restart: unless-stopped` em tudo, derrube a máquina e confirme que o sistema volta sozinho.
3. Script de backup: `docker compose exec db pg_dump -U ghanor ghanor > backup_$(date +%F).sql` agendado no cron. **Teste a restauração** — backup não testado é loteria.
4. No Metabase (com o usuário read-only!), monte um dashboard: personagens por classe, nível médio, sessões por campanha.

---

# APÊNDICE A — Ordem de implementação sugerida (mapa de sprints)

Cada "sprint" cabe em 1–3 semanas do seu ritmo part-time:

| Sprint | Partes | Entregável concreto |
|---|---|---|
| 1 | 1–2 | Repo estruturado, CI verde, ADR commitado |
| 2 | 3–4 | Domínio de atributos + máquina de estados testados |
| 3 | 5–6 | Banco modelado, catálogo carregado via Admin/seed |
| 4 | 7 | API v1 de magias e personagens com permissões |
| 5 | 8 | Ficha na tela: PV/PM interativos + busca de magias |
| 6 | 9 | Wizard completo — **o coração do MVP** |
| 7 | 10 | Sessão: inventário, condições, subir de nível |
| 8 | 11 | Campanhas, tela do mestre |
| 9 | 12 | Deploy no home lab — **MVP no ar** 🎉 |

Regra de sobrevivência do dev solo: **termine o sprint antes de embelezar**. Feito > perfeito, e cada sprint entrega algo demonstrável.

# APÊNDICE B — Trilha pós-MVP (opcional)

Na ordem de melhor retorno:

1. **Uma tela em React** consumindo a API DRF existente (ex.: a tela de sessão) — o comparativo HTMX vs. React na *mesma* funcionalidade é uma história excelente para entrevistas.
2. **Cache com Redis** para o catálogo de regras (dados quase imutáveis = caso ideal de cache).
3. **Observabilidade**: logging estruturado JSON + Prometheus/Grafana no Compose.
4. **Kubernetes** (k3s no home lab) — só depois de sentir na pele o que o Compose não resolve.

# APÊNDICE C — Checklist de qualidade contínua

Antes de cada merge na `main`:

- [ ] `uv run pytest` — tudo verde
- [ ] `uv run ruff check . && uv run ruff format --check .`
- [ ] Nenhum segredo no diff (`git diff --staged | grep -iE "secret|password|key"`)
- [ ] Regra de negócio nova? Está em `dominio/`, com teste, sem import de Django
- [ ] Migration nova? Rodou `migrate` do zero num banco limpo?
- [ ] Commit segue Conventional Commits

---

*Boa jornada, e que os dados rolem a seu favor. 🎲*
