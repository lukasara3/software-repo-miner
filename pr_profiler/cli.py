import typer
from rich.console import Console

app = typer.Typer()
console = Console()

@app.command()
def analyze(repo: str):
    """
    Analisa um repositório do GitHub.
    """
    console.print(f"[bold green]Iniciando análise do repositório:[/bold green] {repo}")
    console.print(":rocket: Setup concluído com sucesso!")

if __name__ == "__main__":
    app()