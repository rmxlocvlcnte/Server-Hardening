# Arquitetura do projeto

## Principios

- Separacao entre coleta, execucao de hardening e comparacao de resultados.
- Politicas declarativas em JSON para facilitar versionamento e auditoria.
- Camada de deteccao de distribuicao para suportar expansao futura.

## Modulos

- `distribuicoes.py`: identifica familia de pacotes e limita escopo suportado.
- `coletor.py`: coleta baseline tecnico do host.
- `executor.py`: aplica a politica de hardening.
- `ansible.py`: gera/roda playbook Ansible a partir da mesma politica.
- `auditoria.py`: compara snapshots e calcula diferencas.
- `relatorio.py`: gera saida em markdown para evidencias.
- `cli.py`: orquestra comandos.

## Seguranca operacional

- Antes de executar alteracoes, o fluxo exibe preview declarativo das mudancas planejadas.
- A aplicacao efetiva depende de confirmacao explicita do administrador (`SIM`), com opcao de bypass controlado para automacao (`--auto-confirmar`).

## Adaptabilidade

Para suportar Fedora/DNF no futuro:

1. Estender `detectar_sistema`.
2. Criar funcoes de execucao especificas para `dnf` e `firewalld`.
3. Manter o mesmo formato de politica, com ajustes opcionais por distro.
