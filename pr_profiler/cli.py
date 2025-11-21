import typer
import sys
from rich.console import Console
from pr_profiler.analysis import run_analysis
from pr_profiler.presentation import display_report

app = typer.Typer(no_args_is_help=True)
console = Console()

@app.callback()
def main():
    """PR Profiler CLI"""
    pass

@app.command()
def analyze(repo: str):
    """
    Analisa um repositório em busca de problemas de processo.
    """
    console.print(f"[bold blue]Iniciando PR Profiler para:[/bold blue] {repo}")

    try:
        # O 'with console.status' cria a animação de carregamento
        with console.status("[bold green]Minerando dados do GitHub API... (Isso pode levar alguns segundos)[/bold green]", spinner="dots"):
            report = run_analysis(repo)
        
        display_report(report)

    except ValueError as e:
        console.print(f"\n[bold red]❌ Erro:[/bold red] {str(e)}")
        sys.exit(1)
        
    except Exception as e:
        console.print(f"\n[bold red]💥 Erro Inesperado:[/bold red] {str(e)}")
        sys.exit(1)

if __name__ == "_main_":
    app()