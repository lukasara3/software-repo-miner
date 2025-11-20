import os
from github import Github
from dotenv import load_dotenv
from pr_profiler.models import PRMetadata  
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def fetch_last_prs(repo_name: str, limit: int = 10) -> list[PRMetadata]:
    if not GITHUB_TOKEN:
        print("❌ Erro: GITHUB_TOKEN não configurado.")
        return []

    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(repo_name)

        print(f"🔄 Conectando a {repo_name} e baixando PRs...")

        # Converte o PaginatedList para lista normal
        prs_list = list(repo.get_pulls(state='all', sort='created', direction='desc'))

        if not prs_list:
            print("⚠️ Nenhum Pull Request encontrado no repositório.")
            return []

        # Limita ao número solicitado
        prs_raw = prs_list[:limit]

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

    except Exception as e:
        print(f"❌ Erro na API: {e}")
        return []
