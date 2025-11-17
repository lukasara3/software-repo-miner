import os
from github import Github
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def run_simple_test():
    """
    Teste básico de conexão.
    Não baixa PRs, apenas verifica se o token acessa o repo.
    """
    print("--- INICIANDO TESTE DE CONEXÃO ---")

    if not GITHUB_TOKEN:
        print("❌ ERRO: Token não encontrado. Verifique seu arquivo .env")
        return

    try:
        g = Github(GITHUB_TOKEN)

        user = g.get_user()
        print(f"✅ Autenticado como: {user.login}")

        repo_name = "andrehora/software-repo-mining"
        repo = g.get_repo(repo_name)
        
        print(f"✅ Repositório encontrado: {repo.full_name}")
        print(f"📝 Descrição: {repo.description}")
        print(f"⭐ Estrelas: {repo.stargazers_count}")
        
        print("--- SUCESSO! O TOKEN ESTÁ FUNCIONANDO ---")

    except Exception as e:
        print(f"❌ FALHA: {e}")

if __name__ == "__main__":
    run_simple_test()