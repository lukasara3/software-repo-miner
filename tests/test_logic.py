from datetime import datetime, timedelta, timezone
from pr_profiler.models import PRMetadata, RepoReport, PRAnalysis
from pr_profiler.analysis import analyze_pr

# --- AJUDANTES PARA CRIAR DADOS FALSOS ---
def create_mock_pr(
    days_old=0, 
    comments=0, 
    additions=0, 
    deletions=0, 
    state='open'
) -> PRMetadata:
    """Cria um PR falso para facilitar os testes"""
    # Adicionamos hours=4 para compensar fuso horário e garantir a virada do dia
    create_date = datetime.now(timezone.utc) - timedelta(days=days_old, hours=4)
    
    return PRMetadata(
        number=1,
        title="Teste PR",
        author="dev_teste",
        created_at=create_date,
        closed_at=None,
        merged_at=None,
        additions=additions,
        deletions=deletions,
        files_changed=1,
        comments_count=comments,
        state=state,
        is_merged=False
    )

# --- BATERIA DE TESTES EXISTENTE (1-12) ---

def test_age_in_days_calc():
    pr = create_mock_pr(days_old=10)
    assert pr.age_in_days == 10

def test_detect_ghost_pr():
    pr = create_mock_pr(days_old=31, comments=0, state='open')
    analysis = analyze_pr(pr)
    assert analysis is not None
    assert analysis.category == "👻 Ghost PR"
    assert analysis.severity == "High"

def test_ignore_ghost_pr_with_comments():
    pr = create_mock_pr(days_old=31, comments=1, state='open')
    analysis = analyze_pr(pr)
    assert analysis is None 

def test_ignore_ghost_pr_recent():
    pr = create_mock_pr(days_old=5, comments=0, state='open')
    analysis = analyze_pr(pr)
    assert analysis is None

def test_detect_wall_of_text():
    pr = create_mock_pr(additions=600, deletions=500)
    analysis = analyze_pr(pr)
    assert analysis is not None
    assert analysis.category == "🧱 Wall of Text"
    assert analysis.severity == "Medium"

def test_ignore_wall_of_text_small():
    pr = create_mock_pr(additions=100, deletions=100)
    analysis = analyze_pr(pr)
    assert analysis is None

def test_detect_bikeshedding():
    pr = create_mock_pr(comments=45, additions=5, deletions=5)
    analysis = analyze_pr(pr)
    assert analysis is not None
    assert analysis.category == "🚲 Bikeshedding"
    assert analysis.severity == "Low"

def test_ignore_bikeshedding_normal():
    pr = create_mock_pr(comments=10, additions=5, deletions=5)
    analysis = analyze_pr(pr)
    assert analysis is None

def test_priority_ghost_over_others():
    pr = create_mock_pr(days_old=40, comments=0, additions=10, deletions=10)
    analysis = analyze_pr(pr)
    assert analysis.category == "👻 Ghost PR"

def test_health_score_perfect():
    report = RepoReport(repo_name="test", total_scanned=0, analyzed_prs=[])
    assert report.health_score == 100

def test_health_score_penalized():
    dummy_analysis = PRAnalysis(create_mock_pr(), "Bad", "Reason", "High")
    problems = [dummy_analysis] * 5
    report = RepoReport(repo_name="test", total_scanned=10, analyzed_prs=problems)
    assert report.health_score == 50

def test_health_score_not_negative():
    dummy_analysis = PRAnalysis(create_mock_pr(), "Bad", "Reason", "High")
    problems = [dummy_analysis] * 20 
    report = RepoReport(repo_name="test", total_scanned=10, analyzed_prs=problems)
    assert report.health_score == 0

# --- NOVOS TESTES (13-17) ---

# 13. Teste Review Vacuum: Detectar PR parado entre 7 e 30 dias
def test_detect_review_vacuum():
    # 15 dias, sem comentários (não é Ghost ainda, mas é Vacuum)
    pr = create_mock_pr(days_old=15, comments=0, state='open')
    analysis = analyze_pr(pr)
    assert analysis is not None
    assert analysis.category == "🕸️ Review Vacuum"
    assert analysis.severity == "Medium"

# 14. Teste Limite Ghost vs Vacuum: Exatamente 30 dias
def test_boundary_ghost_vs_vacuum():
    # A regra do Ghost é > 30. Então 30 dias EXATOS deve ser Vacuum.
    pr = create_mock_pr(days_old=30, comments=0, state='open')
    analysis = analyze_pr(pr)
    assert analysis.category == "🕸️ Review Vacuum"

# 15. Teste Limite Vacuum vs Saudável: Exatamente 7 dias
def test_boundary_vacuum_vs_healthy():
    # A regra do Vacuum é > 7. Então 7 dias EXATOS deve ser saudável.
    pr = create_mock_pr(days_old=7, comments=0, state='open')
    analysis = analyze_pr(pr)
    assert analysis is None

# 16. Teste Vacuum Ignorado: Se tiver comentário, não é vácuo
def test_ignore_vacuum_with_comments():
    pr = create_mock_pr(days_old=20, comments=1, state='open')
    analysis = analyze_pr(pr)
    assert analysis is None

# 17. Teste JSON Export: Verifica se a estrutura do dicionário está certa
def test_repo_report_to_dict():
    # Cria um relatório com 1 problema
    mock_pr = create_mock_pr(days_old=40)
    analysis = PRAnalysis(mock_pr, "👻 Ghost PR", "Old", "High")
    report = RepoReport("user/repo", 10, [analysis])
    
    data = report.to_dict()
    
    # Verifica se as chaves principais existem
    assert "repo_name" in data
    assert "metrics" in data
    assert "problems" in data
    assert data["metrics"]["health_score"] == 90 # 1 problema em 10
    assert data["problems"][0]["category"] == "👻 Ghost PR"