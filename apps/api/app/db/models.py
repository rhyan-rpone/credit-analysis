import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class CaseStatus(str, enum.Enum):
    draft = "draft"
    processing = "processing"
    completed = "completed"
    failed = "failed"


class DocumentStatus(str, enum.Enum):
    uploaded = "uploaded"
    extracted = "extracted"
    failed = "failed"


class Decision(str, enum.Enum):
    approve = "approve"
    reject = "reject"
    manual_review = "manual_review"


class CreditCase(Base):
    __tablename__ = "credit_cases"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    cnpj: Mapped[str | None] = mapped_column(String(32))
    requested_amount: Mapped[float | None] = mapped_column(Float)
    status: Mapped[CaseStatus] = mapped_column(Enum(CaseStatus), default=CaseStatus.draft)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    documents: Mapped[list["Document"]] = relationship(back_populates="credit_case")


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    credit_case_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("credit_cases.id"), nullable=False)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[str] = mapped_column(String(120), nullable=False)
    storage_path: Mapped[str] = mapped_column(Text, nullable=False)
    sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[DocumentStatus] = mapped_column(Enum(DocumentStatus), default=DocumentStatus.uploaded)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    credit_case: Mapped[CreditCase] = relationship(back_populates="documents")


class DocumentExtraction(Base):
    __tablename__ = "document_extractions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("documents.id"), nullable=False)
    raw_text: Mapped[str] = mapped_column(Text, nullable=False)
    extracted_fields: Mapped[dict] = mapped_column(JSONB, default=dict)
    tables: Mapped[list] = mapped_column(JSONB, default=list)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class FinancialIndicator(Base):
    __tablename__ = "financial_indicators"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    credit_case_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("credit_cases.id"), nullable=False)
    indicators: Mapped[dict] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class RiskFlag(Base):
    __tablename__ = "risk_flags"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    credit_case_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("credit_cases.id"), nullable=False)
    code: Mapped[str] = mapped_column(String(80), nullable=False)
    severity: Mapped[str] = mapped_column(String(32), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    evidence: Mapped[dict] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class PolicyResult(Base):
    __tablename__ = "policy_results"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    credit_case_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("credit_cases.id"), nullable=False)
    policy_version: Mapped[str] = mapped_column(String(40), nullable=False)
    results: Mapped[list] = mapped_column(JSONB, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class AgentRun(Base):
    __tablename__ = "agent_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    credit_case_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("credit_cases.id"), nullable=False)
    agent_name: Mapped[str] = mapped_column(String(80), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    input_snapshot: Mapped[dict] = mapped_column(JSONB, default=dict)
    output_snapshot: Mapped[dict] = mapped_column(JSONB, default=dict)
    duration_ms: Mapped[int | None] = mapped_column(Integer)
    error_message: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    credit_case_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("credit_cases.id"), nullable=False)
    decision: Mapped[Decision] = mapped_column(Enum(Decision), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    evidence: Mapped[dict] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Modelos de dados da aplicação (SQLAlchemy ORM).
#
# Este arquivo define a estrutura do banco de dados do sistema de análise
# de crédito baseado em IA.
#
# Cada classe representa uma tabela do PostgreSQL.
#
# Fluxo geral da análise:
#
# 1. Um caso de crédito (CreditCase) é criado.
# 2. Documentos são enviados (Document).
# 3. O OCR extrai informações dos documentos (DocumentExtraction).
# 4. Indicadores financeiros são calculados (FinancialIndicator).
# 5. Riscos identificados são registrados (RiskFlag).
# 6. As políticas de crédito são avaliadas (PolicyResult).
# 7. Os agentes de IA executam suas análises (AgentRun).
# 8. Uma recomendação final é gerada (Recommendation).
#
# Além disso, o arquivo define ENUMs que padronizam os possíveis
# status, decisões e estados do processo.
#
# Benefícios:
# - Estrutura organizada do banco.
# - Relacionamentos automáticos entre tabelas.
# - Consultas mais simples utilizando SQLAlchemy.
# - Histórico completo da execução dos agentes e decisões.