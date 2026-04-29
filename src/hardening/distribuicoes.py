from __future__ import annotations

from pathlib import Path

from .modelos import SistemaDetectado


def detectar_sistema() -> SistemaDetectado:
    arquivo_os_release = Path("/etc/os-release")
    if not arquivo_os_release.exists():
        raise RuntimeError("Nao foi possivel detectar a distribuicao.")

    conteudo = arquivo_os_release.read_text(encoding="utf-8")
    linhas = [linha.strip() for linha in conteudo.splitlines() if linha.strip()]
    mapa = {}
    for linha in linhas:
        if "=" not in linha:
            continue
        chave, valor = linha.split("=", maxsplit=1)
        mapa[chave] = valor.strip('"')

    id_distribuicao = mapa.get("ID", "desconhecida")
    id_like = mapa.get("ID_LIKE", "")

    base_debian = "debian" in id_distribuicao or "debian" in id_like or "ubuntu" in id_distribuicao
    if base_debian:
        return SistemaDetectado(id_distribuicao=id_distribuicao, familia_pacotes="apt")

    # Placeholder para futuras familias (dnf, pacman etc.)
    return SistemaDetectado(id_distribuicao=id_distribuicao, familia_pacotes="desconhecida")
