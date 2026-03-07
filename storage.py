import json
import os

from models import _migrar

ARQUIVO = "tarefas.json"


def carregar_tarefas() -> list:
    if os.path.exists(ARQUIVO):
        try:
            with open(ARQUIVO, "r", encoding="utf-8") as f:
                tarefas = json.load(f)
            return [_migrar(t, i + 1) for i, t in enumerate(tarefas)]
        except (json.JSONDecodeError, OSError):
            return []
    return []


def salvar_tarefas(tarefas: list) -> None:
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(tarefas, f, ensure_ascii=False, indent=2)
