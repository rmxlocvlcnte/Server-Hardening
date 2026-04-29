from __future__ import annotations

import json
import subprocess
from pathlib import Path

from .distribuicoes import detectar_sistema


def _rodar(comando: list[str]) -> tuple[int, str, str]:
    processo = subprocess.run(comando, capture_output=True, text=True, check=False)
    return processo.returncode, processo.stdout, processo.stderr


def _desativar_servicos(servicos: list[str]) -> list[dict]:
    resultados = []
    for servico in servicos:
        codigo, saida, erro = _rodar(["sudo", "systemctl", "disable", "--now", servico])
        resultados.append(
            {
                "acao": "desativar_servico",
                "servico": servico,
                "codigo_saida": codigo,
                "saida": saida.strip(),
                "erro": erro.strip(),
            }
        )
    return resultados


def _configurar_ufw(politica: dict) -> list[dict]:
    resultados = []
    resultados.append(_executar_acao("ufw_padrao_entrada", ["sudo", "ufw", "default", politica.get("politica_padrao_entrada", "deny"), "incoming"]))
    resultados.append(_executar_acao("ufw_padrao_saida", ["sudo", "ufw", "default", politica.get("politica_padrao_saida", "allow"), "outgoing"]))

    for porta in politica.get("portas_permitidas", []):
        resultados.append(_executar_acao(f"ufw_permitir_{porta}", ["sudo", "ufw", "allow", str(porta)]))

    if politica.get("habilitar_ufw", True):
        resultados.append(_executar_acao("ufw_habilitar", ["sudo", "ufw", "--force", "enable"]))

    return resultados


def _endurecer_ssh_se_necessario(politica: dict) -> list[dict]:
    if not politica.get("permitir_ssh_apenas_com_chave", False):
        return []

    arquivo = Path("/etc/ssh/sshd_config")
    texto = arquivo.read_text(encoding="utf-8")
    if "PasswordAuthentication no" not in texto:
        texto += "\nPasswordAuthentication no\n"
        Path("/tmp/sshd_config_hardening").write_text(texto, encoding="utf-8")
        return [
            _executar_acao(
                "copiar_sshd_config",
                ["sudo", "cp", "/tmp/sshd_config_hardening", "/etc/ssh/sshd_config"],
            ),
            _executar_acao("reiniciar_ssh", ["sudo", "systemctl", "restart", "ssh"]),
        ]
    return [{"acao": "ssh_ja_endurecido", "codigo_saida": 0, "saida": "PasswordAuthentication ja desativado", "erro": ""}]


def _executar_acao(nome_acao: str, comando: list[str]) -> dict:
    codigo, saida, erro = _rodar(comando)
    return {
        "acao": nome_acao,
        "comando": " ".join(comando),
        "codigo_saida": codigo,
        "saida": saida.strip(),
        "erro": erro.strip(),
    }


def carregar_politica(caminho_politica: str) -> dict:
    return json.loads(Path(caminho_politica).read_text(encoding="utf-8"))


def gerar_preview_execucao(caminho_politica: str) -> dict:
    sistema = detectar_sistema()
    if sistema.familia_pacotes != "apt":
        raise RuntimeError(
            f"Distribuicao '{sistema.id_distribuicao}' ainda nao suportada. "
            "No momento, apenas sistemas baseados em apt sao suportados."
        )

    politica = carregar_politica(caminho_politica)
    passos = []

    for servico in politica.get("servicos_desativar", []):
        passos.append(
            {
                "acao": "desativar_servico",
                "descricao": f"Desativar e parar servico {servico}",
                "comando_previsto": f"sudo systemctl disable --now {servico}",
            }
        )

    passos.append(
        {
            "acao": "ufw_padrao_entrada",
            "descricao": "Aplicar politica padrao de entrada no UFW",
            "comando_previsto": (
                "sudo ufw default "
                f"{politica.get('politica_padrao_entrada', 'deny')} incoming"
            ),
        }
    )
    passos.append(
        {
            "acao": "ufw_padrao_saida",
            "descricao": "Aplicar politica padrao de saida no UFW",
            "comando_previsto": (
                "sudo ufw default "
                f"{politica.get('politica_padrao_saida', 'allow')} outgoing"
            ),
        }
    )

    for porta in politica.get("portas_permitidas", []):
        passos.append(
            {
                "acao": f"ufw_permitir_{porta}",
                "descricao": f"Permitir trafego na porta {porta}",
                "comando_previsto": f"sudo ufw allow {porta}",
            }
        )

    if politica.get("habilitar_ufw", True):
        passos.append(
            {
                "acao": "ufw_habilitar",
                "descricao": "Habilitar firewall UFW",
                "comando_previsto": "sudo ufw --force enable",
            }
        )

    if politica.get("permitir_ssh_apenas_com_chave", False):
        passos.append(
            {
                "acao": "ssh_desabilitar_senha",
                "descricao": "Garantir PasswordAuthentication no no sshd_config",
                "comando_previsto": "editar /etc/ssh/sshd_config e reiniciar ssh",
            }
        )

    return {
        "politica": politica.get("nome_politica", "sem_nome"),
        "distribuicao": sistema.id_distribuicao,
        "passos_previstos": passos,
    }


def aplicar_politica(caminho_politica: str) -> dict:
    sistema = detectar_sistema()
    if sistema.familia_pacotes != "apt":
        raise RuntimeError(
            f"Distribuicao '{sistema.id_distribuicao}' ainda nao suportada. "
            "No momento, apenas sistemas baseados em apt sao suportados."
        )

    politica = carregar_politica(caminho_politica)
    resultados = []
    resultados.extend(_desativar_servicos(politica.get("servicos_desativar", [])))
    resultados.extend(_configurar_ufw(politica))
    resultados.extend(_endurecer_ssh_se_necessario(politica))

    return {
        "politica": politica.get("nome_politica", "sem_nome"),
        "distribuicao": sistema.id_distribuicao,
        "resultado": resultados,
    }
