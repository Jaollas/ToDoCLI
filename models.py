from datetime import date, datetime

PRIORIDADES = ["alta", "media", "baixa"]
PRIORIDADE_ORDEM = {"alta": 0, "media": 1, "baixa": 2}
PRIORIDADE_ICONE = {"alta": "🔴", "media": "🟡", "baixa": "🟢"}
CATEGORIAS_PADRÃO = ["Trabalho", "Estudo", "Pessoal", "Saúde", "Finanças", "Outro"]


def _migrar(t: dict, fallback_id: int) -> dict:
    return {
        "id": t.get("id", fallback_id),
        "titulo": t.get("titulo", ""),
        "descricao": t.get("descricao", ""),
        "prioridade": t.get("prioridade", "media"),
        "categoria": t.get("categoria", "Outro"),
        "concluida": t.get("concluida", False),
        "data_criacao": t.get("data_criacao") or t.get("criada_em", str(date.today())),
        "prazo": t.get("prazo", ""),
    }


def proximo_id(tarefas: list) -> int:
    return max((t["id"] for t in tarefas), default=0) + 1


def parse_prazo(prazo_str: str):
    try:
        return datetime.strptime(prazo_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def ordenar(tarefas: list) -> list:
    def chave(t):
        p = PRIORIDADE_ORDEM.get(t["prioridade"], 9)
        prazo = parse_prazo(t["prazo"]) or date(9999, 12, 31)
        return (p, prazo)
    return sorted(tarefas, key=chave)


def num_para_id(tarefas: list, num: int):
    ordenados = ordenar(tarefas)
    if 1 <= num <= len(ordenados):
        return ordenados[num - 1]["id"]
    return None


def por_id(tarefas: list, tid: int):
    return next((t for t in tarefas if t["id"] == tid), None)
