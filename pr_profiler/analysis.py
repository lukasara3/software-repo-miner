from typing import List, Optional
from pr_profiler.models import PRMetadata, PRAnalysis, RepoReport
from pr_profiler.github_service import fetch_last_prs

def analyze_pr(pr: PRMetadata) -> Optional[PRAnalysis]:
    """
    Aplica regras para diagnosticar um único PR.
    Retorna um PRAnalysis se houver um problema, ou None se estiver saudável.
    """
    # Regra 1: Ghost PR (Fantasma)
    # Definição: Aberto, mais de 15 dias, 0 comentários.
    if pr.state == 'open' and pr.age_in_days > 15 and pr.comments_count == 0:
        return PRAnalysis(
            metadata=pr,
            category="👻 Ghost PR",
            reason=f"Aberto há {pr.age_in_days} dias sem nenhuma interação.",
            severity="High"
        )
    
    return None

def run_analysis(repo_name: str) -> RepoReport:
    """
    Orquestra a busca e análise completa.
    """
    # 1. Busca dados (Dev 2)
    raw_prs = fetch_last_prs(repo_name, limit=20)
    
    # 2. Aplica lógica (Dev 1)
    analyzed_prs = []
    for pr in raw_prs:
        analysis = analyze_pr(pr)
        if analysis:
            analyzed_prs.append(analysis)
        else:
            # Opcional: Adicionar PRs saudáveis como "Healthy" se quiser mostrar tudo
            pass 
            
    return RepoReport(repo_name=repo_name, analyzed_prs=analyzed_prs)