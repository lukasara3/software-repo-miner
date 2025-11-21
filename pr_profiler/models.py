from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

# dados brutos
@dataclass
class PRMetadata:
    """
    Dados brutos de um Pull Request extraídos do GitHub.
    """
    number: int
    title: str
    author: str
    created_at: datetime
    closed_at: Optional[datetime]
    merged_at: Optional[datetime]
    
    # Métricas
    additions: int
    deletions: int
    files_changed: int
    comments_count: int
    
    # Status
    state: str
    is_merged: bool

    @property
    def age_in_days(self) -> int:
        """Calcula idade do PR em dias corridos"""
        end_date = self.closed_at or datetime.now()
        # Ajuste de fuso horário simples para evitar erros
        if self.created_at.tzinfo:
            end_date = end_date.replace(tzinfo=self.created_at.tzinfo)
        delta = end_date - self.created_at
        return delta.days

# dados para analise
@dataclass
class PRAnalysis:
    """
    Representa o diagnóstico de um único PR.
    """
    metadata: PRMetadata  
    category: str         
    reason: str           
    severity: str        

@dataclass
class RepoReport:
    """
    Relatório final consolidado.
    Agora com suporte a métricas agregadas.
    """
    repo_name: str
    total_scanned: int 
    analyzed_prs: List[PRAnalysis]
    
    @property
    def health_score(self) -> int:
        """Calcula uma 'nota' de 0 a 100 para o processo"""
        if self.total_scanned == 0:
            return 100
        problem_count = len(self.analyzed_prs)
        # Penaliza 5 pontos por problema, mínimo 0
        score = 100 - (problem_count / self.total_scanned * 100)
        return int(max(0, score))