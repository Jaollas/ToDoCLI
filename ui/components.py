import os
from datetime import date

from rich import box
from rich.panel import Panel
from rich.prompt import Confirm, IntPrompt, Prompt
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

from models import PRIORIDADE_ICONE, PRIORIDADE_ORDEM, CATEGORIAS_PADRÃO, PRIORIDADES, ordenar, parse_prazo
from ui.theme import APP_TITLE, console

FILTROS = {"todas": None, "pendentes": False, "concluídas": True}


def limpar(subtitulo: str = "") -> None:
    os.system("cls" if os.name == "nt" else "clear")
    console.print(Panel(f"[title]{APP_TITLE}[/title]", border_style="cyan", padding=(0, 2)))
    if subtitulo:
        console.print(Rule(f"[key]{subtitulo}[/key]", style="cyan"))
    console.print()


def aguardar() -> None:
    console.print()
    console.input("[muted]  Pressione [bold]Enter[/bold] para voltar ao menu...[/muted]")

def resumo_prazo(prazo_str: str) -> Text:
    prazo = parse_prazo(prazo_str)
    if prazo is None:
        return Text("—", style="muted")
    hoje = date.today()
    diff = (prazo - hoje).days
    if diff < 0:
        return Text(f"⚠ atrasada {abs(diff)}d", style="overdue")
    if diff == 0:
        return Text("🔥 vence hoje", style="due.today")
    if diff == 1:
        return Text("📅 vence amanhã", style="due.soon")
    if diff <= 7:
        return Text(f"📅 vence em {diff}d", style="due.soon")
    return Text(f"📅 {prazo.strftime('%d/%m/%Y')}", style="due.ok")


def resumo_status(tarefas: list) -> str:
    total = len(tarefas)
    concluidas = sum(1 for t in tarefas if t["concluida"])
    pendentes = total - concluidas
    atrasadas = sum(
        1 for t in tarefas
        if not t["concluida"] and parse_prazo(t["prazo"]) and parse_prazo(t["prazo"]) < date.today()
    )
    txt = (
        f"[done]{concluidas} concluída(s)[/done]  "
        f"[pending]{pendentes} pendente(s)[/pending]  "
        f"[muted]{total} total[/muted]"
    )
    if atrasadas:
        txt += f"  [overdue]⚠ {atrasadas} atrasada(s)[/overdue]"
    return txt

def tabela_tarefas(tarefas: list, filtro: str = "todas") -> None:
    estado = FILTROS[filtro]
    lista = [t for t in ordenar(tarefas) if estado is None or t["concluida"] == estado]

    if not lista:
        console.print(f"[muted]  Nenhuma tarefa [{filtro}] encontrada.[/muted]")
        return

    idx_map = {t["id"]: i + 1 for i, t in enumerate(ordenar(tarefas))}

    tb = Table(box=box.ROUNDED, border_style="cyan", header_style="title", expand=True)
    tb.add_column("#", style="muted", width=4, justify="right")
    tb.add_column("P", width=3, justify="center")
    tb.add_column("Categoria", width=12)
    tb.add_column("Tarefa")
    tb.add_column("Prazo", width=20)

    for tarefa in lista:
        cat_text = Text(f"[{tarefa['categoria']}]", style="cat")
        if tarefa["concluida"]:
            titulo_text = Text(tarefa["titulo"], style="done strike")
        else:
            titulo_text = Text(tarefa["titulo"])
            if tarefa.get("descricao"):
                titulo_text.append(f"\n  {tarefa['descricao']}", style="muted")
        tb.add_row(
            str(idx_map[tarefa["id"]]),
            PRIORIDADE_ICONE.get(tarefa["prioridade"], ""),
            cat_text,
            titulo_text,
            resumo_prazo(tarefa["prazo"]),
        )

    console.print(tb)
    console.print(
        f"\n[muted]  {len(lista)} tarefa(s) · filtro: [bold]{filtro}[/bold] · ordenadas por prioridade[/muted]"
    )

def pedir_prioridade(default: str = "media") -> str:
    console.print("  [pri.alta]alta[/pri.alta]  [pri.media]media[/pri.media]  [pri.baixa]baixa[/pri.baixa]")
    return Prompt.ask("[key]Prioridade[/key]", choices=PRIORIDADES, default=default, show_choices=False)


def pedir_categoria(default: str = "Outro") -> str:
    opts = "  ".join(f"[cat]{c}[/cat]" for c in CATEGORIAS_PADRÃO)
    console.print(f"  {opts}")
    return Prompt.ask("[key]Categoria[/key]", default=default)


def pedir_prazo(default: str = "") -> str:
    from datetime import datetime
    while True:
        valor = Prompt.ask("[key]Prazo[/key] (AAAA-MM-DD ou deixe vazio)", default=default).strip()
        if not valor:
            return ""
        try:
            datetime.strptime(valor, "%Y-%m-%d")
            return valor
        except ValueError:
            console.print("[danger]⚠  Formato inválido. Use AAAA-MM-DD.[/danger]")
