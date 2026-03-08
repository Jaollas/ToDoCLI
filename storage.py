"""Persistence layer — load and save the tasks JSON file."""
import json
import os

ARQUIVO = "tarefas.json"


def carregar_tarefas() -> list:
    if os.path.exists(ARQUIVO):
        try:
            with open(ARQUIVO, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return []
    return []


def salvar_tarefas(tarefas: list) -> None:
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(tarefas, f, ensure_ascii=False, indent=2)
