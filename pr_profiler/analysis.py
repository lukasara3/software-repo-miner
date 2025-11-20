from typing import List, Optional
from pr_profiler.models import PRMetadata, PRAnalysis, RepoReport
from pr_profiler.github_service import fetch_last_prs

def analyze_pr(pr: PRMetadata) -> Optional[PRAnalysis]:
    """
    Aplica regras para diagnosticar um único PR.
    """
    # 1. Ghost PR (Fantasma)
    if pr.state == 'open' and pr.age_in_days > 30 and pr.comments_count == 0:
        return PRAnalysis(
            metadata=pr,
            category="👻 Ghost PR",
            reason=f"Aberto há {pr.age_in_days} dias sem interação.",
            severity="High"
        )

    # 2. Wall of Text (Muro de Texto)
    # Regra: Mais de 1000 linhas alteradas (soma de add + del)
    total_changes = pr.additions + pr.deletions
    if total_changes > 1000:
        return PRAnalysis(
            metadata=pr,
            category="🧱 Wall of Text",
            reason=f"PR Gigante: {total_changes} linhas alteradas. Difícil de revisar.",
            severity="Medium"
        )

    # 3. Bikeshedding (Discussão Trivial Excessiva)
    # Regra: Muitas discussões (ex: > 40 comentários) em um PR pequeno/médio (< 200 linhas)
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
    raw_prs = fetch_last_prs(repo_name, limit=30)
    
    analyzed_prs = []
    for pr in raw_prs:
        analysis = analyze_pr(pr)
        if analysis:
            analyzed_prs.append(analysis)
        else:
            pass 
            
    return RepoReport(repo_name=repo_name, analyzed_prs=analyzed_prs)