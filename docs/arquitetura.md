# Arquitetura do projeto

## Principios

- Separação entre coleta, execução de hardening e comparação de resultados.
- Políticas declarativas em JSON para facilitar versionamento e auditoria.
- Camada de detecção de distribuição para suportar expansão futura.

## Modulos

- `distribuicoes.py`: identifica família de pacotes e limita escopo suportado.
- `coletor.py`: coleta baseline técnico do host.
- `executor.py`: aplica a política de hardening.
- `ansible.py`: gera/roda playbook Ansible a partir da mesma política.
- `auditoria.py`: compara snapshots e calcula diferenças.
- `relatorio.py`: gera saída em markdown para evidências.
- `cli.py`: orquestra comandos.

## Seguranca operacional

- Antes de executar alteraçõess, o fluxo exibe preview declarativo das mudancas planejadas.
- A aplicação efetiva depende de confirmação explícita do administrador (`SIM`), com opção de bypass controlado para automacao (`--auto-confirmar`).

## Adaptabilidade

Para suportar Fedora/DNF no futuro:

1. Estender `detectar_sistema`.
2. Criar funções de execução específicas para `dnf` e `firewalld`.
3. Manter o mesmo formato de política, com ajustes opcionais por distro.
