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
    # CORREÇÃO: Adicionamos hours=4 para compensar fuso horário (UTC vs Local)
    # Isso garante que "10 dias" sejam "10 dias e 4 horas", evitando o arredondamento para 9
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

# --- BATERIA DE TESTES (12 Testes) ---

# 1. Teste de cálculo de dias (Models)
def test_age_in_days_calc():
    pr = create_mock_pr(days_old=10)
    # Agora deve ser 10 com certeza
    assert pr.age_in_days == 10

# 2. Teste Ghost PR: Deve detectar quando for velho e sem comentários
def test_detect_ghost_pr():
    pr = create_mock_pr(days_old=31, comments=0, state='open')
    analysis = analyze_pr(pr)
    assert analysis is not None
    assert analysis.category == "👻 Ghost PR"
    assert analysis.severity == "High"

# 3. Teste Ghost PR: NÃO deve detectar se tiver comentários
def test_ignore_ghost_pr_with_comments():
    pr = create_mock_pr(days_old=31, comments=1, state='open')
    analysis = analyze_pr(pr)
    assert analysis is None  # É saudável

# 4. Teste Ghost PR: NÃO deve detectar se for recente
def test_ignore_ghost_pr_recent():
    pr = create_mock_pr(days_old=5, comments=0, state='open')
    analysis = analyze_pr(pr)
    assert analysis is None

# 5. Teste Wall of Text: Deve detectar PR gigante
def test_detect_wall_of_text():
    # 600 add + 500 del = 1100 linhas (> 1000)
    pr = create_mock_pr(additions=600, deletions=500)
    analysis = analyze_pr(pr)
    assert analysis is not None
    assert analysis.category == "🧱 Wall of Text"
    assert analysis.severity == "Medium"

# 6. Teste Wall of Text: NÃO deve detectar PR pequeno
def test_ignore_wall_of_text_small():
    pr = create_mock_pr(additions=100, deletions=100)
    analysis = analyze_pr(pr)
    assert analysis is None

# 7. Teste Bikeshedding: Deve detectar muita discussão em pouca mudança
def test_detect_bikeshedding():
    # 45 comments, 10 linhas alteradas
    pr = create_mock_pr(comments=45, additions=5, deletions=5)
    analysis = analyze_pr(pr)
    assert analysis is not None
    assert analysis.category == "🚲 Bikeshedding"
    assert analysis.severity == "Low"

# 8. Teste Bikeshedding: NÃO deve detectar se a discussão for proporcional
def test_ignore_bikeshedding_normal():
    # 10 comments, 10 linhas alteradas (não atinge limite de 40 comments)
    pr = create_mock_pr(comments=10, additions=5, deletions=5)
    analysis = analyze_pr(pr)
    assert analysis is None

# 9. Teste Prioridade: Ghost PR deve ser retornado mesmo se for pequeno
def test_priority_ghost_over_others():
    # É velho, sem comments, e pequeno. Deve ser Ghost.
    pr = create_mock_pr(days_old=40, comments=0, additions=10, deletions=10)
    analysis = analyze_pr(pr)
    assert analysis.category == "👻 Ghost PR"

# 10. Teste Health Score: 100% se lista vazia
def test_health_score_perfect():
    report = RepoReport(repo_name="test", total_scanned=0, analyzed_prs=[])
    assert report.health_score == 100

# 11. Teste Health Score: Penalidade funciona
def test_health_score_penalized():
    # 10 escaneados, 5 problemáticos = 50% problemas -> score 50
    dummy_analysis = PRAnalysis(create_mock_pr(), "Bad", "Reason", "High")
    problems = [dummy_analysis] * 5
    report = RepoReport(repo_name="test", total_scanned=10, analyzed_prs=problems)
    assert report.health_score == 50

# 12. Teste Health Score: Não pode ser negativo
def test_health_score_not_negative():
    dummy_analysis = PRAnalysis(create_mock_pr(), "Bad", "Reason", "High")
    problems = [dummy_analysis] * 20 # 20 problemas em 10 scanneados
    report = RepoReport(repo_name="test", total_scanned=10, analyzed_prs=problems)
    assert report.health_score == 0 # Mínimo deve ser 0