from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

from .distribuicoes import detectar_sistema


def _bloco_ufw(politica: dict) -> list[str]:
    linhas = [
        "    - name: Definir politica padrao de entrada no UFW",
        "      community.general.ufw:",
        f"        direction: incoming",
        f"        policy: {politica.get('politica_padrao_entrada', 'deny')}",
        "",
        "    - name: Definir politica padrao de saida no UFW",
        "      community.general.ufw:",
        f"        direction: outgoing",
        f"        policy: {politica.get('politica_padrao_saida', 'allow')}",
        "",
    ]

    for porta in politica.get("portas_permitidas", []):
        linhas.extend(
            [
                f"    - name: Permitir porta {porta} no UFW",
                "      community.general.ufw:",
                "        rule: allow",
                f"        port: '{porta}'",
                "",
            ]
        )

    if politica.get("habilitar_ufw", True):
        linhas.extend(
            [
                "    - name: Habilitar UFW",
                "      community.general.ufw:",
                "        state: enabled",
                "",
            ]
        )

    return linhas


def _bloco_servicos(politica: dict) -> list[str]:
    servicos = politica.get("servicos_desativar", [])
    if not servicos:
        return []

    return [
        "    - name: Desativar servicos desnecessarios",
        "      ansible.builtin.systemd:",
        "        name: \"{{ item }}\"",
        "        enabled: false",
        "        state: stopped",
        "      loop:",
        *[f"        - {servico}" for servico in servicos],
        "",
    ]


def _bloco_ssh(politica: dict) -> list[str]:
    if not politica.get("permitir_ssh_apenas_com_chave", False):
        return []

    return [
        "    - name: Desabilitar autenticacao por senha no SSH",
        "      ansible.builtin.lineinfile:",
        "        path: /etc/ssh/sshd_config",
        "        regexp: '^#?PasswordAuthentication\\s+'",
        "        line: 'PasswordAuthentication no'",
        "        create: false",
        "",
        "    - name: Reiniciar servico SSH",
        "      ansible.builtin.systemd:",
        "        name: ssh",
        "        state: restarted",
        "",
    ]


def gerar_playbook_ansible(caminho_politica: str, caminho_saida: str) -> Path:
    sistema = detectar_sistema()
    if sistema.familia_pacotes != "apt":
        raise RuntimeError(
            f"Distribuicao '{sistema.id_distribuicao}' ainda nao suportada. "
            "No momento, apenas sistemas baseados em apt sao suportados."
        )

    politica = json.loads(Path(caminho_politica).read_text(encoding="utf-8"))
    linhas = [
        "---",
        f"# Politica: {politica.get('nome_politica', 'sem_nome')}",
        "- name: Hardening Linux baseado em politica declarativa",
        "  hosts: all",
        "  become: true",
        "  gather_facts: true",
        "  tasks:",
        *(_bloco_servicos(politica)),
        *(_bloco_ufw(politica)),
        *(_bloco_ssh(politica)),
    ]
    conteudo = "\n".join(linhas).rstrip() + "\n"

    destino = Path(caminho_saida)
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(conteudo, encoding="utf-8")
    return destino


def executar_playbook_ansible(caminho_playbook: str, inventario: str) -> dict:
    if shutil.which("ansible-playbook") is None:
        raise RuntimeError(
            "Comando 'ansible-playbook' nao encontrado. "
            "Instale o Ansible antes de executar o playbook."
        )

    comando = ["ansible-playbook", "-i", inventario, caminho_playbook]
    processo = subprocess.run(comando, capture_output=True, text=True, check=False)
    return {
        "comando": " ".join(comando),
        "codigo_saida": processo.returncode,
        "saida": processo.stdout.strip(),
        "erro": processo.stderr.strip(),
    }
