from rich.console import Console
from rich.table import Table
from pr_profiler.models import RepoReport

console = Console()

def display_report(report: RepoReport):
    """
    Imprime o relatório de diagnósticos no terminal.
    """
    console.print(f"\n[bold blue]Relatório de Análise: {report.repo_name}[/bold blue]")
    
    if not report.analyzed_prs:
        console.print("[green]Parabéns! Nenhum problema crítico detectado nos últimos PRs.[/green]")
        return

    table = Table(title="Problemas Detectados")

    table.add_column("PR #", style="cyan", no_wrap=True)
    table.add_column("Diagnóstico", style="bold red")
    table.add_column("Severidade", justify="center")
    table.add_column("Motivo", style="white")
    table.add_column("Link", style="blue")

    for item in report.analyzed_prs:
        # Define cor da severidade
        sev_color = "red" if item.severity == "High" else "yellow"
        
        table.add_row(
            str(item.metadata.number),
            item.category,
            f"[{sev_color}]{item.severity}[/{sev_color}]",
            item.reason,
            f"github.com/{report.repo_name}/pull/{item.metadata.number}"
        )

    console.print(table)