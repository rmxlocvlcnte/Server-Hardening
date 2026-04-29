# Metodologia de avaliacao antes/depois

## 1. Baseline (antes)

- Coletar servicos habilitados.
- Coletar portas em escuta.
- Coletar status do firewall.
- Executar `lynis audit system` e registrar resultados.

## 2. Aplicacao do hardening

- Aplicar politica definida em JSON.
- Registrar log de cada acao.

## 3. Pos-hardening (depois)

- Repetir coleta dos mesmos indicadores do baseline.
- Comparar diferencas e validar reducao de exposicao.

## 4. Criterios de sucesso

- Reducao de servicos nao essenciais habilitados.
- Reducao de portas abertas desnecessarias.
- Firewall ativo e com politica restritiva de entrada.
- Politicas de acesso remoto endurecidas (ex.: senha SSH desativada).
