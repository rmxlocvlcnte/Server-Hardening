# Projeto de Hardening Linux (PT-BR)

Implementacao de processo de hardening em servidores Linux com foco inicial em distribuicoes baseadas em Debian (`apt`), com arquitetura preparada para expansao futura para Fedora (`dnf`) e outras distros.

## Objetivos

- Reduzir superficie de ataque por meio de hardening automatizado.
- Aplicar boas praticas de seguranca defensiva:
  - desativacao de servicos desnecessarios;
  - configuracao de firewall;
  - restricao de portas;
  - fortalecimento de politicas de acesso.
- Comparar estado antes/depois com varreduras de seguranca.
- Documentar processo de forma replicavel.

## Escopo atual

- Distro-alvo inicial: Debian/Ubuntu e derivadas com `apt`.
- Linguagem principal: Python.
- Suporte opcional a scripts shell para operacoes de sistema.

## Estrutura do repositorio

```text
projeto-hardening-linux/
  docs/
    arquitetura.md
    metodologia-avaliacao.md
    playbook-validacao.md
  exemplos/
    politica_hardening_debian.json
  scripts/
    instalar_dependencias.sh
  src/
    cli.py
    hardening/
      __init__.py
      auditoria.py
      coletor.py
      distribuicoes.py
      executor.py
      modelos.py
      relatorio.py
  pyproject.toml
```

## Fluxo recomendado

1. Coletar baseline do servidor (`auditar`).
2. Aplicar hardening (`aplicar`).
3. Executar nova auditoria.
4. Gerar comparativo (`comparar`).
5. Registrar evidencias e licoes aprendidas.

## Uso rapido

### 1) Instalar dependencias

```bash
bash scripts/instalar_dependencias.sh
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 2) Rodar auditoria inicial

```bash
hardener auditar --saida artefatos/baseline.json
```

### 3) Aplicar hardening

```bash
hardener aplicar --politica exemplos/politica_hardening_debian.json
```

O comando `aplicar` agora sempre mostra um preview das mudancas e pede confirmacao do administrador (`SIM`) antes de executar.
Para somente inspecionar sem alterar nada:

```bash
hardener aplicar --politica exemplos/politica_hardening_debian.json --preview
```

### 4) Rodar auditoria final e comparar

```bash
hardener auditar --saida artefatos/pos_hardening.json
hardener comparar --antes artefatos/baseline.json --depois artefatos/pos_hardening.json --saida artefatos/comparativo.md
```

### 5) Gerar playbook Ansible da mesma politica

```bash
hardener ansible --politica exemplos/politica_hardening_debian.json --saida-playbook artefatos/hardening.yml
```

Para executar diretamente no host local:

```bash
hardener ansible --politica exemplos/politica_hardening_debian.json --executar --inventario localhost,
```

Na execucao do playbook com `--executar`, tambem ha confirmacao interativa por padrao.
Para cenarios automatizados (CI/CD), use `--auto-confirmar`.

## Exemplo de uso em ambiente profissional

Cenário típico: executar hardening em um servidor de produção durante uma janela de manutenção, com aprovação formal do administrador e geração de evidências para auditoria.

1. Preparar diretório de evidências

```bash
mkdir -p artefatos
```

2. Coletar baseline (antes das mudanças)

```bash
hardener auditar --saida artefatos/baseline.json
```

3. Gerar preview das mudanças e submeter para aprovação

```bash
hardener aplicar --politica exemplos/politica_hardening_debian.json --preview
```

Depois que o administrador validar o preview, executar a aplicação efetiva (o comando exige `SIM` para continuar):

```bash
hardener aplicar --politica exemplos/politica_hardening_debian.json
```

4. Coletar auditoria pós-mudança e produzir comparativo

```bash
hardener auditar --saida artefatos/pos_hardening.json
hardener comparar --antes artefatos/baseline.json --depois artefatos/pos_hardening.json --saida artefatos/comparativo.md
```

5. (Opcional) Gerar playbook Ansible a partir da mesma política

```bash
hardener ansible --politica exemplos/politica_hardening_debian.json --saida-playbook artefatos/hardening.yml
```

Para executar o playbook em um inventário profissional (apenas após aprovação):

```bash
hardener ansible --politica exemplos/politica_hardening_debian.json --executar --inventario inventories/producao.ini
```

Observação: para automação (CI/CD), use `--auto-confirmar` somente quando a aprovação já tiver sido registrada externamente (mudança aprovada, ticket/OSW, janela de manutenção etc.).

## Ferramentas sugeridas para validacao

- `ss -tulpen` (servicos/portas)
- `systemctl list-unit-files --type=service`
- `nmap` (visao externa, quando permitido)
- `lynis` (auditoria local de seguranca)

> Importante: execute apenas em ambientes autorizados.

## Visão Futura (Roadmap)

O projeto esta estruturado para evoluir de forma incremental, mantendo a politica declarativa como fonte principal de verdade e reforcando dois pilares: **auditabilidade** (o que foi alterado e por que) e **seguranca operacional** (preview + aprovacao antes de aplicar).

### Curto prazo (governanca e previsibilidade)

- Expandir a politica atual com validacoes mais detalhadas para servicos, firewall e SSH.
- Melhorar o preview operacional para indicar impacto esperado, risco estimado e possiveis dependencias entre mudancas.
- Enriquecer os relatorios com mais contexto tecnico para facilitar auditoria e troubleshooting.
- Adicionar testes automatizados para os fluxos principais da CLI e para a geracao de playbooks.

### Medio prazo (escala e padronizacao)

- Evoluir a integracao com Ansible para usar `roles`, `templates` e organizacao por responsabilidades.
- Suportar perfis por papel de servidor, como `web`, `banco`, `bastion` e `jump host`.
- Preparar um fluxo de aprovacao formal (ex.: registrar um identificador de ticket/OSW e manter trilha de auditoria).
- Incluir capacidade de detectar drift entre o estado esperado da politica e o estado real do host.

### Longo prazo (conformidade e resiliência)

- Suportar outras distribuicoes, comecando por Fedora/RHEL (`dnf`) e derivados.
- Mapear controles para benchmarks reconhecidos, como CIS, para facilitar conformidade e evidencias.
- Incorporar rollback orientado por politica para mudancas seguras e reversiveis quando possivel.
- Preparar operacao em multiplos hosts com inventarios, grupos e ambientes distintos.

### Linhas de evolucao contínua

- Integracao com pipelines de CI/CD para validacao de politica antes da execucao.
- Exportacao de evidencias em formatos consumiveis por times de governanca e compliance.
- Catalogo de politicas versionadas por ambiente, criticidade e tipo de ativo.
- Dashboards ou resumos executivos para acompanhamento de postura de hardening ao longo do tempo.

### Objetivo final

Transformar hardening em um processo repetivel, mensuravel e governado por politica, com baixa friccao para operacoes e alta confianca para auditoria.
