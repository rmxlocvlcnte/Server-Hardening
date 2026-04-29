from dataclasses import dataclass


@dataclass
class SistemaDetectado:
    id_distribuicao: str
    familia_pacotes: str


@dataclass
class ResultadoComando:
    comando: str
    codigo_saida: int
    saida: str
    erro: str
