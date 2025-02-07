from enum import Enum

from pydantic import BaseModel, Field


class Clause(BaseModel):
    """Identified legal provision with contextual metadata"""

    clause_id: int = Field(..., description="Unique identifier for the clause")
    name: str = Field(
        ...,
        min_length=3,
        description="Standardized name of clause type from legal taxonomy",
    )
    text: str = Field(
        ...,
        min_length=50,
        description="Exact verbatim text of identified clause including punctuation",
    )


class RiskLevel(Enum):
    """Risk assessment level for identified clause"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskAssessment(BaseModel):
    """Risk assessment for identified clause"""

    clause_id: int = Field(..., description="Unique identifier of the clause being assessed")
    risk_level: RiskLevel = Field(..., description="Risk assessment level for the clause")
    risk_description: str = Field(..., min_length=50, description="Detailed risk analysis")
    risk_category: str = Field(..., description="Risk category, e.g., Regulatory, Financial, Operational")
