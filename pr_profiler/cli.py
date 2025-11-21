import typer
import sys
import json
from rich.console import Console
from typing import Optional
from pr_profiler.analysis import run_analysis
from pr_profiler.presentation import display_report

app = typer.Typer(no_args_is_help=True)
console = Console()

@app.callback()
def main():
    """PR Profiler CLI"""
    pass

@app.command()
def analyze(
    repo: str, 
    json_out: Optional[str] = typer.Option(None, "--json", "-j", help="Caminho para salvar o relatório em JSON.")
):
    """
    Analisa um repositório. Use --json para salvar o resultado em arquivo.
    """
    console.print(f"[bold blue]Iniciando PR Profiler para:[/bold blue] {repo}")

    try:
        with console.status("[bold green]Minerando dados...[/bold green]", spinner="dots"):
            report = run_analysis(repo)
        
        # 1. Sempre mostra na tela (visualização rica)
        display_report(report)

        # 2. Se o usuário pediu JSON, salva o arquivo
        if json_out:
            data = report.to_dict()
            with open(json_out, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            
            console.print(f"\n[bold green]💾 Relatório salvo com sucesso em: {json_out}[/bold green]")

    except Exception as e:
        console.print(f"\n[bold red]💥 Erro:[/bold red] {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    app()