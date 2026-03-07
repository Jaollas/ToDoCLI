from datetime import datetime

from fpdf import FPDF, XPos, YPos

from models import ordenar, PRIORIDADE_ICONE
from ui.components import limpar, aguardar
from ui.theme import console

_COR_PRI = {"alta": (220, 50, 50), "media": (200, 150, 0), "baixa": (40, 160, 40)}


def tela_exportar_pdf(tarefas: list) -> None:
    limpar("Exportar Tarefas Abertas para PDF")
    abertas = [t for t in ordenar(tarefas) if not t["concluida"]]
    if not abertas:
        console.print("[muted]  Nenhuma tarefa aberta para exportar.[/muted]")
        aguardar()
        return

    nome_arquivo = f"tarefas_abertas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(20, 20, 20)

    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(0, 180, 200)
    pdf.cell(0, 12, "To-Do List - Tarefas Abertas",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 6, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(8)

    for i, t in enumerate(abertas, 1):
        r, g, b = _COR_PRI.get(t["prioridade"], (120, 120, 120))
        pdf.set_fill_color(r, g, b)
        pdf.rect(20, pdf.get_y(), 3, 14, "F")
        pdf.set_xy(25, pdf.get_y())
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(30, 30, 30)
        pdf.cell(8, 7, f"{i}.", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(0, 7, t["titulo"], new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.set_x(33)
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(100, 100, 100)
        meta = f"[{t['categoria']}]  Prioridade: {t['prioridade']}"
        if t.get("prazo"):
            meta += f"  |  Prazo: {t['prazo']}"
        pdf.cell(0, 5, meta, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        if t.get("descricao"):
            pdf.set_x(33)
            pdf.set_font("Helvetica", "I", 8)
            pdf.set_text_color(130, 130, 130)
            pdf.multi_cell(0, 4, t["descricao"])

        pdf.ln(4)

        if i < len(abertas):
            pdf.set_draw_color(220, 220, 220)
            pdf.line(20, pdf.get_y(), 190, pdf.get_y())
            pdf.ln(4)

    pdf.set_y(-20)
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(160, 160, 160)
    pdf.cell(0, 5, f"{len(abertas)} tarefa(s) abertas", align="C")

    pdf.output(nome_arquivo)
    console.print(f"[done]📄  PDF gerado: [bold]{nome_arquivo}[/bold][/done]")
    aguardar()
