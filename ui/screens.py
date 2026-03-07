from datetime import date

from rich import box
from rich.prompt import Confirm, IntPrompt, Prompt
from rich.table import Table
from rich.text import Text

from logger import ACAO_COR, ACAO_ICONE, carregar_logs, registrar_log
from models import PRIORIDADE_ICONE, num_para_id, por_id, proximo_id
from storage import salvar_tarefas
from ui.components import (
    aguardar,
    limpar,
    pedir_categoria,
    pedir_prazo,
    pedir_prioridade,
    resumo_prazo,
    resumo_status,
    tabela_tarefas,
)
from ui.theme import console

def tela_menu(tarefas: list) -> str:
    limpar()
    console.print(f"  {resumo_status(tarefas)}\n")
    opcoes = [
        ("1", "Listar tarefas"),
        ("2", "Adicionar tarefa"),
        ("3", "Editar tarefa"),
        ("4", "Concluir tarefa"),
        ("5", "Remover tarefa"),
        ("6", "Histórico de atividades"),
        ("7", "Exportar abertas para PDF"),
        ("0", "Sair"),
    ]
    for k, v in opcoes:
        console.print(f"  [key]{k}[/key]  {v}")
    console.print()
    return Prompt.ask("[key]Opção[/key]", choices=[k for k, _ in opcoes], show_choices=False)

def tela_listar(tarefas: list) -> None:
    limpar("Listar Tarefas")
    console.print("  [key]a[/key] Todas   [key]p[/key] Pendentes   [key]c[/key] Concluídas\n")
    opcao = Prompt.ask("[key]Filtro[/key]", choices=["a", "p", "c"], default="a", show_choices=False)
    filtro = {"a": "todas", "p": "pendentes", "c": "concluídas"}[opcao]
    limpar(f"Listar Tarefas — {filtro.capitalize()}")
    tabela_tarefas(tarefas, filtro)
    aguardar()

def tela_adicionar(tarefas: list) -> None:
    limpar("Adicionar Tarefa")
    titulo = Prompt.ask("[key]Título[/key]").strip()
    if not titulo:
        console.print("[danger]⚠  Título não pode ser vazio.[/danger]")
        aguardar()
        return
    descricao = Prompt.ask("[key]Descrição[/key] (opcional)", default="").strip()
    console.print()
    prioridade = pedir_prioridade()
    console.print()
    categoria = pedir_categoria()
    console.print()
    prazo = pedir_prazo()

    nova = {
        "id": proximo_id(tarefas),
        "titulo": titulo,
        "descricao": descricao,
        "prioridade": prioridade,
        "categoria": categoria,
        "concluida": False,
        "data_criacao": str(date.today()),
        "prazo": prazo,
    }
    tarefas.append(nova)
    salvar_tarefas(tarefas)
    registrar_log("criada", nova)

    limpar("Adicionar Tarefa")
    console.print("[done]✅  Tarefa adicionada![/done]\n")
    console.print(f"  [key]Título[/key]      {titulo}")
    console.print(f"  [key]Categoria[/key]   [{categoria}]")
    console.print(f"  [key]Prioridade[/key]  {PRIORIDADE_ICONE[prioridade]} {prioridade}")
    if prazo:
        console.print(f"  [key]Prazo[/key]       {resumo_prazo(prazo)}")
    aguardar()

def tela_editar(tarefas: list) -> None:
    limpar("Editar Tarefa")
    if not tarefas:
        console.print("[muted]  Nenhuma tarefa cadastrada.[/muted]")
        aguardar()
        return

    tabela_tarefas(tarefas)
    console.print()
    num = IntPrompt.ask("[key]Número da tarefa[/key]")
    tid = num_para_id(tarefas, num)
    if tid is None:
        console.print("[danger]⚠  Número inválido.[/danger]")
        aguardar()
        return

    t = por_id(tarefas, tid)
    limpar("Editar Tarefa")
    console.print(
        f"  Editando: [bold]{t['titulo']}[/bold]  "
        f"[cat][{t['categoria']}][/cat]  {PRIORIDADE_ICONE[t['prioridade']]} {t['prioridade']}\n"
    )

    t["titulo"] = Prompt.ask("[key]Título[/key]", default=t["titulo"]).strip() or t["titulo"]
    t["descricao"] = Prompt.ask("[key]Descrição[/key]", default=t.get("descricao", "")).strip()
    console.print()
    t["prioridade"] = pedir_prioridade(default=t["prioridade"])
    console.print()
    t["categoria"] = pedir_categoria(default=t["categoria"])
    console.print()
    t["prazo"] = pedir_prazo(default=t.get("prazo", ""))

    salvar_tarefas(tarefas)
    registrar_log("editada", t)
    console.print(f"\n[done]✏️   Tarefa '[bold]{t['titulo']}[/bold]' atualizada![/done]")
    aguardar()

def tela_concluir(tarefas: list) -> None:
    limpar("Concluir Tarefa")
    if not any(not t["concluida"] for t in tarefas):
        console.print("[done]🎉  Todas as tarefas já estão concluídas![/done]")
        aguardar()
        return

    tabela_tarefas(tarefas, filtro="pendentes")
    console.print()
    num = IntPrompt.ask("[key]Número da tarefa[/key]")
    tid = num_para_id(tarefas, num)
    if tid is None:
        console.print("[danger]⚠  Número inválido.[/danger]")
        aguardar()
        return

    t = por_id(tarefas, tid)
    if t["concluida"]:
        console.print("[muted]  Essa tarefa já está concluída.[/muted]")
        aguardar()
        return
    t["concluida"] = True
    salvar_tarefas(tarefas)
    registrar_log("concluída", t)
    console.print(f"\n[done]✅  '[bold]{t['titulo']}[/bold]' concluída![/done]")
    aguardar()

def tela_remover(tarefas: list) -> None:
    limpar("Remover Tarefa")
    if not tarefas:
        console.print("[muted]  Nenhuma tarefa cadastrada.[/muted]")
        aguardar()
        return

    tabela_tarefas(tarefas)
    console.print()
    num = IntPrompt.ask("[key]Número da tarefa[/key]")
    tid = num_para_id(tarefas, num)
    if tid is None:
        console.print("[danger]⚠  Número inválido.[/danger]")
        aguardar()
        return

    t = por_id(tarefas, tid)
    limpar("Remover Tarefa")
    console.print(
        f"  Tarefa selecionada: [bold danger]{t['titulo']}[/bold danger]  [cat][{t['categoria']}][/cat]\n"
    )
    if Confirm.ask("[danger]Confirmar remoção?[/danger]", default=False):
        registrar_log("removida", t)
        tarefas[:] = [x for x in tarefas if x["id"] != tid]
        salvar_tarefas(tarefas)
        console.print("\n[danger]🗑️   Tarefa removida.[/danger]")
    else:
        console.print("\n[muted]  Operação cancelada.[/muted]")
    aguardar()

def tela_historico(_tarefas: list) -> None:
    limpar("Histórico de Atividades")
    logs = carregar_logs()
    if not logs:
        console.print("[muted]  Nenhuma atividade registrada ainda.[/muted]")
        aguardar()
        return

    tb = Table(box=box.ROUNDED, border_style="cyan", header_style="title", expand=True)
    tb.add_column("Data/Hora", style="muted", width=17)
    tb.add_column("Ação", width=11)
    tb.add_column("#", style="muted", width=4, justify="right")
    tb.add_column("Tarefa")

    for entrada in reversed(logs):
        acao = entrada["acao"]
        cor = ACAO_COR.get(acao, "white")
        icone = ACAO_ICONE.get(acao, "")
        tb.add_row(
            entrada["timestamp"],
            Text(f"{icone} {acao}", style=cor),
            str(entrada["tarefa_id"]),
            entrada["titulo"],
        )

    console.print(tb)
    console.print(f"\n[muted]  {len(logs)} evento(s) · mais recentes primeiro[/muted]")
    aguardar()
