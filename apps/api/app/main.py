from fastapi import FastAPI

from app.api.cases import router as cases_router
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title="Analista de Credito Multiagente",
    version="0.1.0",
)

app.include_router(cases_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "env": settings.app_env}