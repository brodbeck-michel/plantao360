from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database.session import get_db
from app.core.config import get_settings

router = APIRouter()
settings = get_settings()


@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    db_status = "disconnected"
    status_code = 200

    try:
        db.execute(text("SELECT 1"))
        db.commit()
        db_status = "connected"
    except Exception:
        db_status = "disconnected"
        status_code = 503

    response_data = {
        "status": "ok" if db_status == "connected" else "error",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "database": db_status,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    return JSONResponse(content=response_data, status_code=status_code)
