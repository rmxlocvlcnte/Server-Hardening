from __future__ import annotations

from pathlib import Path


def gerar_relatorio_markdown(comparativo: dict, caminho_saida: str) -> Path:
    caminho = Path(caminho_saida)
    caminho.parent.mkdir(parents=True, exist_ok=True)

    conteudo = [
        "# Relatorio comparativo de hardening",
        "",
        "## Servicos",
        f"- Removidos: {', '.join(comparativo.get('servicos_removidos', [])) or 'nenhum'}",
        f"- Adicionados: {', '.join(comparativo.get('servicos_adicionados', [])) or 'nenhum'}",
        "",
        "## Portas",
        f"- Fechadas: {', '.join(comparativo.get('portas_fechadas', [])) or 'nenhuma'}",
        f"- Abertas: {', '.join(comparativo.get('portas_abertas', [])) or 'nenhuma'}",
        "",
        "## Interpretacao",
        "- O objetivo e reduzir servicos e portas expostas sem impactar os requisitos operacionais.",
        "- Revise qualquer nova porta aberta e confirme se ela e realmente necessaria.",
    ]
    caminho.write_text("\n".join(conteudo) + "\n", encoding="utf-8")
    return caminho
