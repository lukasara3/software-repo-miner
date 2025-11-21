from typing import Optional
from pr_profiler.models import PRMetadata, PRAnalysis, RepoReport
from pr_profiler.github_service import fetch_last_prs

def analyze_pr(pr: PRMetadata) -> Optional[PRAnalysis]:
    """
    Aplica regras para diagnosticar um único PR.
    Retorna um PRAnalysis se houver um problema, ou None se estiver saudável.
    """
    # Ghost PR (Fantasma) 
    # Aberto, abandonado há mais de 30 dias sem interação.
    if pr.state == 'open' and pr.age_in_days > 30 and pr.comments_count == 0:
        return PRAnalysis(
            metadata=pr,
            category="👻 Ghost PR",
            reason=f"Abandonado há {pr.age_in_days} dias sem nenhuma interação.",
            severity="High"
        )

    # Review Vacuum (O PR Vácuo)
    # Aberto, sem resposta há mais de 7 dias (mas menos que 30, senão seria Ghost).
    # Isso indica que o desenvolvedor está bloqueado esperando code review.
    if pr.state == 'open' and pr.age_in_days > 7 and pr.comments_count == 0:
        return PRAnalysis(
            metadata=pr,
            category="🕸️ Review Vacuum",
            reason=f"Bloqueado: Aguardando primeira revisão há {pr.age_in_days} dias.",
            severity="Medium"
        )

    # Wall of Text (Muro de Texto)
    # Mais de 1000 linhas alteradas (soma de add + del)
    total_changes = pr.additions + pr.deletions
    if total_changes > 1000:
        return PRAnalysis(
            metadata=pr,
            category="🧱 Wall of Text",
            reason=f"PR Gigante: {total_changes} linhas alteradas. Difícil de revisar.",
            severity="Medium"
        )

    # Bikeshedding (Discussão Trivial Excessiva)
    # Muitas discussões (ex: > 40 comentários) em um PR pequeno (< 200 linhas)
    if pr.comments_count > 40 and total_changes < 200:
        return PRAnalysis(
            metadata=pr,
            category="🚲 Bikeshedding",
            reason=f"Muita discussão ({pr.comments_count} comments) para pouca mudança.",
            severity="Low"
        )

    return None

def run_analysis(repo_name: str) -> RepoReport:
    """
    Orquestra a busca e análise completa.
    """
    # Busca 50 PRs para ter uma amostra estatística melhor
    raw_prs = fetch_last_prs(repo_name, limit=50)
    
    analyzed_prs = []
    for pr in raw_prs:
        analysis = analyze_pr(pr)
        if analysis:
            analyzed_prs.append(analysis)
            
    # Retorna o relatório com o total scanneado
    return RepoReport(
        repo_name=repo_name, 
        total_scanned=len(raw_prs), 
        analyzed_prs=analyzed_prs
    )