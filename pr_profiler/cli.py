import typer
from rich.console import Console
from pr_profiler.analysis import get_pr_titles

app = typer.Typer(no_args_is_help=True)
console = Console()

@app.callback()
def main():
    """
    PR Profiler: Ferramenta de Mineração de Repositórios.
    Use os comandos abaixo para analisar repositórios.
    """
    pass

@app.command()
def analyze(repo: str):
    """
    Hello World: Lista os títulos dos últimos 10 PRs.
    """
    console.print(f"[bold blue]Analisando repositório:[/bold blue] {repo}")
    
    # Chama a camada de lógica 
    titles = get_pr_titles(repo)
    
    if not titles:
        console.print("[red]Nenhum PR encontrado ou erro na busca.[/red]")
        return

    console.print("\n[bold green]Últimos 10 Pull Requests:[/bold green]")
    for title in titles:
        console.print(f" - {title}")

if __name__ == "__main__":
    app()