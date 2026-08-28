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