from export import tela_exportar_pdf
from storage import carregar_tarefas
from ui.screens import (
    tela_adicionar,
    tela_concluir,
    tela_editar,
    tela_historico,
    tela_listar,
    tela_menu,
    tela_remover,
)
from ui.theme import console


def main() -> None:
    tarefas = carregar_tarefas()

    telas = {
        "1": tela_listar,
        "2": tela_adicionar,
        "3": tela_editar,
        "4": tela_concluir,
        "5": tela_remover,
        "6": tela_historico,
        "7": tela_exportar_pdf,
    }

    while True:
        opcao = tela_menu(tarefas)
        if opcao == "0":
            from ui.components import limpar
            limpar()
            console.print("[title]👋  Até logo![/title]\n")
            break
        if opcao in telas:
            telas[opcao](tarefas)


if __name__ == "__main__":
    main()
