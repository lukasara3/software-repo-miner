from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from pr_profiler.models import RepoReport

console = Console()

def display_report(report: RepoReport):
    """Imprime relatório com resumo e tabela."""
    
    # 1. Cabeçalho com Métricas Agregadas (Painel)
    count_problems = len(report.analyzed_prs)
    health_color = "green" if report.health_score > 80 else ("yellow" if report.health_score > 50 else "red")
    
    summary_text = Text()
    summary_text.append(f"Repositório: {report.repo_name}\n", style="bold white")
    summary_text.append(f"PRs Analisados: {report.total_scanned}\n", style="white")
    summary_text.append(f"PRs Problemáticos: {count_problems}\n", style="bold red")
    summary_text.append(f"Health Score: {report.health_score}/100", style=f"bold {health_color}")

    console.print(Panel(summary_text, title="📊 Resumo da Análise", expand=False))

    if not report.analyzed_prs:
        console.print("\n[bold green]✨ Tudo limpo! Nenhum anti-padrão detectado na amostra.[/bold green]")
        return

    # 2. Tabela de Detalhes
    table = Table(title="🔍 Diagnósticos Detalhados")
    table.add_column("PR", style="cyan", no_wrap=True)
    table.add_column("Problema", style="bold red")
    table.add_column("Severidade", justify="center")
    table.add_column("Motivo")

    for item in report.analyzed_prs:
        sev_color = "red" if item.severity == "High" else "yellow"
        table.add_row(
            f"#{item.metadata.number}",
            item.category,
            f"[{sev_color}]{item.severity}[/{sev_color}]",
            item.reason
        )

    console.print(table)