import os
from typing import List
from github import Github, GithubException, UnknownObjectException, BadCredentialsException
from dotenv import load_dotenv
from pr_profiler.models import PRMetadata

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def fetch_last_prs(repo_name: str, limit: int = 10) -> List[PRMetadata]:
    if not GITHUB_TOKEN:
        raise ValueError("GITHUB_TOKEN não encontrado no .env")

    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(repo_name)
        
        # Tenta pegar os PRs. Se o repo for privado e o token ruim, falha aqui.
        prs_raw = repo.get_pulls(state='all', sort='created', direction='desc')[:limit]
        
        processed_prs = []
        for pr in prs_raw:
            meta = PRMetadata(
                number=pr.number,
                title=pr.title,
                author=pr.user.login,
                created_at=pr.created_at,
                closed_at=pr.closed_at,
                merged_at=pr.merged_at,
                additions=pr.additions,
                deletions=pr.deletions,
                files_changed=pr.changed_files,
                comments_count=pr.comments,
                state=pr.state,
                is_merged=pr.merged
            )
            processed_prs.append(meta)
            
        return processed_prs

    except UnknownObjectException:
        # Erro 404
        raise ValueError(f"Repositório '{repo_name}' não encontrado. Verifique se o nome está correto (ex: dono/repo).")
    
    except BadCredentialsException:
        # Erro 401
        raise ValueError("Token do GitHub inválido ou expirado. Verifique seu arquivo .env")
        
    except GithubException as e:
        # Outros erros (limite de API, internet, etc)
        raise ValueError(f"Erro de comunicação com o GitHub: {e.data.get('message', str(e))}")