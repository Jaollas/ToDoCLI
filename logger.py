import json
import os
from datetime import datetime

ARQUIVO_LOG = "logs.json"

ACAO_COR = {
    "criada": "done",
    "editada": "pending",
    "concluída": "done",
    "removida": "danger",
}
ACAO_ICONE = {
    "criada": "➕",
    "editada": "✏️ ",
    "concluída": "✅",
    "removida": "🗑️ ",
}


def registrar_log(acao: str, tarefa: dict) -> None:
    entrada = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "acao": acao,
        "tarefa_id": tarefa["id"],
        "titulo": tarefa["titulo"],
    }
    logs: list = []
    if os.path.exists(ARQUIVO_LOG):
        try:
            with open(ARQUIVO_LOG, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except (json.JSONDecodeError, OSError):
            logs = []
    logs.append(entrada)
    with open(ARQUIVO_LOG, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)


def carregar_logs() -> list:
    if not os.path.exists(ARQUIVO_LOG):
        return []
    try:
        with open(ARQUIVO_LOG, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []
