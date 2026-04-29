from __future__ import annotations

import argparse
import json
from pathlib import Path

from hardening.ansible import executar_playbook_ansible, gerar_playbook_ansible
from hardening.auditoria import carregar_auditoria, comparar_auditorias
from hardening.coletor import salvar_coleta
from hardening.executor import aplicar_politica, gerar_preview_execucao
from hardening.relatorio import gerar_relatorio_markdown


def _comando_auditar(argumentos: argparse.Namespace) -> None:
    caminho = salvar_coleta(argumentos.saida)
    print(f"Auditoria salva em: {caminho}")


def _comando_aplicar(argumentos: argparse.Namespace) -> None:
    preview = gerar_preview_execucao(argumentos.politica)
    print(json.dumps(preview, indent=2, ensure_ascii=False))
    if argumentos.preview:
        return
    if not argumentos.auto_confirmar:
        resposta = input("Digite SIM para confirmar aplicacao da politica: ").strip()
        if resposta != "SIM":
            print("Aplicacao cancelada pelo administrador.")
            return
    resultado = aplicar_politica(argumentos.politica)
    print(json.dumps(resultado, indent=2, ensure_ascii=False))


def _comando_comparar(argumentos: argparse.Namespace) -> None:
    antes = carregar_auditoria(argumentos.antes)
    depois = carregar_auditoria(argumentos.depois)
    comparativo = comparar_auditorias(antes, depois)
    caminho_relatorio = gerar_relatorio_markdown(comparativo, argumentos.saida)
    print(f"Comparativo salvo em: {caminho_relatorio}")


def _comando_ansible(argumentos: argparse.Namespace) -> None:
    preview = gerar_preview_execucao(argumentos.politica)
    print(json.dumps(preview, indent=2, ensure_ascii=False))
    caminho_playbook = gerar_playbook_ansible(argumentos.politica, argumentos.saida_playbook)
    print(f"Playbook gerado em: {caminho_playbook}")
    if argumentos.preview:
        return
    if argumentos.executar:
        if not argumentos.auto_confirmar:
            resposta = input("Digite SIM para confirmar execucao do playbook: ").strip()
            if resposta != "SIM":
                print("Execucao do playbook cancelada pelo administrador.")
                return
        resultado = executar_playbook_ansible(str(caminho_playbook), argumentos.inventario)
        print(json.dumps(resultado, indent=2, ensure_ascii=False))


def criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hardener",
        description="Automacao de hardening Linux com foco inicial em Debian/APT",
    )
    subcomandos = parser.add_subparsers(dest="comando", required=True)

    parser_auditar = subcomandos.add_parser("auditar", help="Coleta estado atual de seguranca")
    parser_auditar.add_argument("--saida", required=True, help="Arquivo JSON de saida")
    parser_auditar.set_defaults(funcao=_comando_auditar)

    parser_aplicar = subcomandos.add_parser("aplicar", help="Aplica politica de hardening")
    parser_aplicar.add_argument("--politica", required=True, help="Caminho do JSON de politica")
    parser_aplicar.add_argument(
        "--preview",
        action="store_true",
        help="Somente exibe mudancas previstas, sem executar",
    )
    parser_aplicar.add_argument(
        "--auto-confirmar",
        action="store_true",
        help="Executa sem pedir confirmacao interativa",
    )
    parser_aplicar.set_defaults(funcao=_comando_aplicar)

    parser_comparar = subcomandos.add_parser("comparar", help="Compara auditorias antes/depois")
    parser_comparar.add_argument("--antes", required=True, help="Arquivo de baseline")
    parser_comparar.add_argument("--depois", required=True, help="Arquivo pos-hardening")
    parser_comparar.add_argument("--saida", required=True, help="Relatorio markdown de saida")
    parser_comparar.set_defaults(funcao=_comando_comparar)

    parser_ansible = subcomandos.add_parser(
        "ansible",
        help="Gera playbook Ansible (e opcionalmente executa)",
    )
    parser_ansible.add_argument("--politica", required=True, help="Caminho do JSON de politica")
    parser_ansible.add_argument(
        "--saida-playbook",
        default="artefatos/hardening.yml",
        help="Arquivo YAML do playbook gerado",
    )
    parser_ansible.add_argument(
        "--executar",
        action="store_true",
        help="Executa o playbook via ansible-playbook apos gerar",
    )
    parser_ansible.add_argument(
        "--preview",
        action="store_true",
        help="Somente gera preview e playbook, sem executar",
    )
    parser_ansible.add_argument(
        "--auto-confirmar",
        action="store_true",
        help="Executa sem pedir confirmacao interativa",
    )
    parser_ansible.add_argument(
        "--inventario",
        default="localhost,",
        help="Inventario Ansible (padrao: localhost,)",
    )
    parser_ansible.set_defaults(funcao=_comando_ansible)

    return parser


def main() -> None:
    parser = criar_parser()
    argumentos = parser.parse_args()
    argumentos.funcao(argumentos)


if __name__ == "__main__":
    main()
