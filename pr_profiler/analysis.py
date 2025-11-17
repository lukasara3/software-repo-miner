from typing import List
from pr_profiler.models import PRMetadata
from pr_profiler.github_service import fetch_last_prs

def get_pr_titles(repo_name: str) -> List[str]:
    """
    Função simples inicial: 
    Pede os dados ao serviço e extrai apenas os títulos para exibir.
    """
    # Chama a camada de serviço 
    prs = fetch_last_prs(repo_name, limit=10)
    
    # Extrai só o que interessa para o Hello World (Número e Título)
    titles = [f"#{pr.number}: {pr.title}" for pr in prs]
    return titles