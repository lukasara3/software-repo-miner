import typer
from pr_profiler.analysis import run_analysis
from pr_profiler.presentation import display_report

app = typer.Typer(no_args_is_help=True)

@app.callback()
def main():
    """PR Profiler CLI"""
    pass

@app.command()
def analyze(repo: str):
    """
    Analisa um repositório em busca de problemas de processo.
    """
    # Chama a lógica (Analysis)
    report = run_analysis(repo)
    
    # Chama a visualização (Presentation)
    display_report(report)

if __name__ == "_main_":
    app()