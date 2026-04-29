from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from .distribuicoes import detectar_sistema


def _executar_comando(comando: list[str]) -> str:
    processo = subprocess.run(comando, capture_output=True, text=True, check=False)
    if processo.returncode != 0:
        return processo.stdout + "\n" + processo.stderr
    return processo.stdout


def coletar_estado_atual() -> dict:
    sistema = detectar_sistema()
    dados = {
        "coletado_em": datetime.now(timezone.utc).isoformat(),
        "distribuicao": sistema.id_distribuicao,
        "familia_pacotes": sistema.familia_pacotes,
        "servicos_habilitados": _executar_comando(["systemctl", "list-unit-files", "--type=service", "--state=enabled"]),
        "portas_escutando": _executar_comando(["ss", "-tulpen"]),
        "status_ufw": _executar_comando(["ufw", "status", "verbose"]),
    }
    return dados


def salvar_coleta(caminho_saida: str) -> Path:
    caminho = Path(caminho_saida)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    dados = coletar_estado_atual()
    caminho.write_text(json.dumps(dados, indent=2, ensure_ascii=False), encoding="utf-8")
    return caminho
