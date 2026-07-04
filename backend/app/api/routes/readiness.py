import os
from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database.session import get_db
from app.core.config import get_settings
from app.database.base import Base

router = APIRouter()
settings = get_settings()


@router.get("/readiness")
def readiness_check(db: Session = Depends(get_db)):
    checks = {
        "database": False,
        "settings": False,
        "storage": False,
        "migrations": False,
    }

    try:
        db.execute(text("SELECT 1"))
        db.commit()
        checks["database"] = True
    except Exception:
        pass

    try:
        _ = settings.DATABASE_URL
        _ = settings.SECRET_KEY
        _ = settings.APP_NAME
        checks["settings"] = True
    except Exception:
        pass

    try:
        data_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data")
        backup_dir = os.path.join(data_dir, "backups")
        os.makedirs(data_dir, exist_ok=True)
        os.makedirs(backup_dir, exist_ok=True)
        checks["storage"] = os.path.isdir(data_dir) and os.path.isdir(backup_dir)
    except Exception:
        pass

    try:
        _ = Base.metadata
        checks["migrations"] = True
    except Exception:
        pass

    all_ready = all(checks.values())

    return {
        "ready": all_ready,
        "checks": checks,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
