from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

# --- DADOS BRUTOS (Vêm do GitHub) ---
@dataclass
class PRMetadata:
    number: int
    title: str
    author: str
    created_at: datetime
    closed_at: Optional[datetime]
    merged_at: Optional[datetime]
    additions: int
    deletions: int
    files_changed: int
    comments_count: int
    state: str
    is_merged: bool

    @property
    def age_in_days(self) -> int:
        end_date = self.closed_at or datetime.now()
        if self.created_at.tzinfo:
            end_date = end_date.replace(tzinfo=self.created_at.tzinfo)
        delta = end_date - self.created_at
        return delta.days

# --- DADOS DE ANÁLISE ---
@dataclass
class PRAnalysis:
    metadata: PRMetadata
    category: str
    reason: str
    severity: str

@dataclass
class RepoReport:
    """
    Relatório final consolidado.
    """
    repo_name: str
    total_scanned: int
    analyzed_prs: List[PRAnalysis]
    
    @property
    def health_score(self) -> int:
        if self.total_scanned == 0: return 100
        problem_count = len(self.analyzed_prs)
        score = 100 - (problem_count / self.total_scanned * 100)
        return int(max(0, score))

    def to_dict(self):
        """Converte o relatório para um dicionário compatível com JSON"""
        return {
            "repo_name": self.repo_name,
            "timestamp": datetime.now().isoformat(),
            "metrics": {
                "total_scanned": self.total_scanned,
                "problem_count": len(self.analyzed_prs),
                "health_score": self.health_score
            },
            "problems": [
                {
                    "pr_number": p.metadata.number,
                    "title": p.metadata.title,
                    "category": p.category,
                    "severity": p.severity,
                    "reason": p.reason,
                    "days_open": p.metadata.age_in_days,
                    "url": f"https://github.com/{self.repo_name}/pull/{p.metadata.number}"
                } for p in self.analyzed_prs
            ]
        }