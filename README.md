# To-Do List CLI

Um gerenciador de tarefas de linha de comando, escrito em Python, com interface rica no terminal via `rich` e exportação para PDF via `fpdf2`.

## Funcionalidades

- **Listar** tarefas com filtro (todas / pendentes / concluídas), ordenadas por prioridade e prazo
- **Adicionar** tarefa com título, descrição, prioridade, categoria e prazo
- **Editar** qualquer campo de uma tarefa existente
- **Concluir** tarefas pendentes
- **Remover** tarefas com confirmação
- **Histórico** de atividades (criar, editar, concluir, remover) salvo em `logs.json`
- **Exportar** tarefas abertas para um PDF formatado

## Requisitos

- Python 3.10+
- Dependências listadas em `requirements.txt`

## Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/todo-list-cli.git
cd todo-list-cli

# (Recomendado) Crie um ambiente virtual
python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate  # Linux / macOS

# Instale as dependências
pip install -r requirements.txt
```

## Uso

```bash
python main.py
```

Navegue pelo menu numérico. Cada ação abre uma tela dedicada que limpa o terminal e exibe apenas o contexto relevante. Pressione **Enter** ao final de qualquer tela para voltar ao menu principal.

## Modelo de dados

Cada tarefa é salva em `tarefas.json` com o seguinte formato:

```json
{
  "id": 1,
  "titulo": "Estudar React",
  "descricao": "Hooks e estado global",
  "prioridade": "alta",
  "categoria": "Estudo",
  "concluida": false,
  "data_criacao": "2026-03-06",
  "prazo": "2026-03-10"
}
```

| Campo | Valores possíveis |
|-------|------------------|
| `prioridade` | `alta` · `media` · `baixa` |
| `categoria` | `Trabalho` · `Estudo` · `Pessoal` · `Saúde` · `Finanças` · `Outro` |

## Estrutura do projeto

```
├── main.py              # Entry point
├── models.py            # Modelo de dados, ordenação e helpers de lookup
├── storage.py           # Leitura e escrita de tarefas.json
├── logger.py            # Sistema de log de atividades (logs.json)
├── export.py            # Geração de PDF
├── requirements.txt
├── .gitignore
└── ui/
    ├── theme.py         # Tema Rich e console singleton
    ├── components.py    # Componentes visuais reutilizáveis
    └── screens.py       # Telas do aplicativo
```

## Arquivos gerados em runtime

| Arquivo | Descrição |
|---------|-----------|
| `tarefas.json` | Base de dados local das tarefas |
| `logs.json` | Histórico de atividades |
| `tarefas_abertas_*.pdf` | PDFs exportados |

Nenhum desses arquivos vai para o repositório (ver `.gitignore`).

## Dependências

```
rich      # Interface de terminal
fpdf2     # Geração de PDF
```
