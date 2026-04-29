# Playbook de validacao operacional

## Checklist rapido

- [ ] Possuo backup/snapshot recente da maquina.
- [ ] Janela de manutencao aprovada.
- [ ] Acesso alternativo ao servidor disponivel.
- [ ] Politica de hardening revisada.

## Execucao

1. `hardener auditar --saida artefatos/baseline.json`
2. `hardener aplicar --politica exemplos/politica_hardening_debian.json --preview`
3. Revisar preview com o administrador do servidor e confirmar a aplicacao.
4. `hardener aplicar --politica exemplos/politica_hardening_debian.json`
5. `hardener auditar --saida artefatos/pos_hardening.json`
6. `hardener comparar --antes artefatos/baseline.json --depois artefatos/pos_hardening.json --saida artefatos/comparativo.md`
7. `hardener ansible --politica exemplos/politica_hardening_debian.json --saida-playbook artefatos/hardening.yml`

## Pos-validacao

- Validar funcionamento dos servicos de negocio.
- Confirmar acesso administrativo autorizado.
- Guardar relatorio e logs como evidencia.
