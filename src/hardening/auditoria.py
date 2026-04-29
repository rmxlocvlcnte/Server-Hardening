from __future__ import annotations

import json
from pathlib import Path


def carregar_auditoria(caminho: str) -> dict:
    return json.loads(Path(caminho).read_text(encoding="utf-8"))


def comparar_auditorias(antes: dict, depois: dict) -> dict:
    servicos_antes = set(_extrair_servicos_habilitados(antes.get("servicos_habilitados", "")))
    servicos_depois = set(_extrair_servicos_habilitados(depois.get("servicos_habilitados", "")))
    removidos = sorted(servicos_antes - servicos_depois)
    adicionados = sorted(servicos_depois - servicos_antes)

    portas_antes = set(_extrair_portas(antes.get("portas_escutando", "")))
    portas_depois = set(_extrair_portas(depois.get("portas_escutando", "")))

    return {
        "servicos_removidos": removidos,
        "servicos_adicionados": adicionados,
        "portas_fechadas": sorted(portas_antes - portas_depois),
        "portas_abertas": sorted(portas_depois - portas_antes),
    }


def _extrair_servicos_habilitados(texto: str) -> list[str]:
    linhas = [linha.strip() for linha in texto.splitlines() if linha.strip()]
    servicos = []
    for linha in linhas:
        if ".service" in linha and "enabled" in linha:
            servicos.append(linha.split()[0])
    return servicos


def _extrair_portas(texto: str) -> list[str]:
    portas = []
    for linha in texto.splitlines():
        partes = linha.split()
        if len(partes) < 5:
            continue
        endereco = partes[4]
        if ":" in endereco:
            portas.append(endereco.split(":")[-1])
    return portas
