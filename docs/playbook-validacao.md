# Playbook de validacao operacional

## Checklist rapido

- [ ] Possuo backup/snapshot recente da maquina.
- [ ] Janela de manutenção aprovada.
- [ ] Acesso alternativo ao servidor disponível.
- [ ] Política de hardening revisada.

## Execucao

1. `hardener auditar --saida artefatos/baseline.json`
2. `hardener aplicar --politica exemplos/politica_hardening_debian.json --preview`
3. Revisar preview com o administrador do servidor e confirmar a aplicação.
4. `hardener aplicar --politica exemplos/politica_hardening_debian.json`
5. `hardener auditar --saida artefatos/pos_hardening.json`
6. `hardener comparar --antes artefatos/baseline.json --depois artefatos/pos_hardening.json --saida artefatos/comparativo.md`
7. `hardener ansible --politica exemplos/politica_hardening_debian.json --saida-playbook artefatos/hardening.yml`

## Pos-validação

- Validar funcionamento dos serviços de negócio.
- Confirmar acesso administrativo autorizado.
- Guardar relatório e logs como evidência.
