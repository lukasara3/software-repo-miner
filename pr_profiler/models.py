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
    Relatório final consolidado do repositório.
    """
    repo_name: str
    analyzed_prs: List[PRAnalysis]
    
    def count_by_category(self, category: str) -> int:
        return sum(1 for pr in self.analyzed_prs if pr.category == category)