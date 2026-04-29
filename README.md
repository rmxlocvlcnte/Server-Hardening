# Projeto de Hardening Linux

Implementação de processo de hardening em servidores Linux com foco inicial em distribuições baseadas em Debian (`apt`), com arquitetura preparada para expansão futura para Fedora (`dnf`) e outras distros.

## Objetivos

- Reduzir superfície de ataque por meio de hardening automatizado.
- Aplicar boas práticas de seguranca defensiva:
  - desativação de servicos desnecessarios;
  - configuração de firewall;
  - restrição de portas;
  - fortalecimento de políticas de acesso.
- Comparar estado antes/depois com varreduras de seguranca.
- Documentar processo de forma replicavel.

## Escopo atual

- Distro-alvo inicial: Debian/Ubuntu e derivadas com `apt`.
- Linguagem principal: Python.
- Suporte opcional a scripts shell para operacoes de sistema.

## Estrutura do repositorio

```
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

## Uso rápido

### 1) Instalar dependências

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

O comando `aplicar` agora sempre mostra um preview das mudanças e pede confirmação do administrador (`SIM`) antes de executar.
Para somente inspecionar sem alterar nada:

```bash
hardener aplicar --politica exemplos/politica_hardening_debian.json --preview
```

### 4) Rodar auditoria final e comparar

```bash
hardener auditar --saida artefatos/pos_hardening.json
hardener comparar --antes artefatos/baseline.json --depois artefatos/pos_hardening.json --saida artefatos/comparativo.md
```

### 5) Gerar playbook Ansible da mesma política

```bash
hardener ansible --politica exemplos/politica_hardening_debian.json --saida-playbook artefatos/hardening.yml
```

Para executar diretamente no host local:

```bash
hardener ansible --politica exemplos/politica_hardening_debian.json --executar --inventario localhost,
```

Na execução do playbook com `--executar`, também há confirmação interativa por padrão.
Para cenários automatizados (CI/CD), use `--auto-confirmar`.

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

- Expandir a política atual com validações mais detalhadas para serviços, firewall e SSH.
- Melhorar o preview operacional para indicar impacto esperado, risco estimado e possíveis dependências entre mudanças.
- Enriquecer os relatórios com mais contexto tecnico para facilitar auditorias e troubleshooting.
- Adicionar testes automatizados para os fluxos principais da CLI e para a geração de playbooks.

### Médio prazo (escala e padronização)

- Evoluir a integração com Ansible para usar `roles`, `templates` e organizacao por responsabilidades.
- Suportar perfis por papel de servidor, como `web`, `banco`, `bastion` e `jump host`.
- Preparar um fluxo de aprovação formal (ex.: registrar um identificador de ticket/OSW e manter trilha de auditoria).
- Incluir capacidade de detectar drift entre a o estado esperado da política e o estado real do host.

### Longo prazo (conformidade e resiliência)

- Suportar outras distribuicoes, começando por Fedora/RHEL (`dnf`) e derivados.
- Mapear controles para benchmarks reconhecidos, como CIS, para facilitar conformidade e evidencias.
- Incorporar rollback orientado por política para mudancas seguras e reversíveis quando possível.
- Preparar operacao em múltiplos hosts com inventários, grupos e ambientes distintos.

### Linhas de evolução contínua

- Integração com pipelines de CI/CD para validação de política antes da execução.
- Exportação de evidências em formatos consumíveis por times de governanca e compliance.
- Catalogo de políticas versionadas por ambiente, criticidade e tipo de ativo.
- Dashboards ou resumos executivos para acompanhamento de postura de hardening ao longo do tempo.

### Objetivo final

Transformar hardening em um processo repetível, mensurável e governado por política, com baixa fricção para operações e alta confiança para auditoria.
