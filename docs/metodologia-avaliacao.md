# Metodologia de avaliacao antes/depois

## 1. Baseline (antes)

- Coletar servicos habilitados.
- Coletar portas em escuta.
- Coletar status do firewall.
- Executar `lynis audit system` e registrar resultados.

## 2. Aplicacao do hardening

- Aplicar política definida em JSON.
- Registrar log de cada acao.

## 3. Pós-hardening (depois)

- Repetir coleta dos mesmos indicadores do baseline.
- Comparar diferenças e validar redução de exposição.

## 4. Criterios de sucesso

- Redução de servicos não essenciais habilitados.
- Redução de portas abertas desnecessárias.
- Firewall ativo e com política restritiva de entrada.
- Políticas de acesso remoto endurecidas (ex.: senha SSH desativada).
