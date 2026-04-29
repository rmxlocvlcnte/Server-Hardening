#!/usr/bin/env bash
set -euo pipefail

echo "[INFO] Atualizando indice de pacotes..."
sudo apt update

echo "[INFO] Instalando ferramentas de auditoria e rede..."
sudo apt install -y python3 python3-venv python3-pip nmap lynis ufw ansible

echo "[INFO] Dependencias basicas instaladas."
