from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Question
from ..schemas.category import Category

router = APIRouter(prefix="/categories", tags=["categories"])

CATEGORY_SEED = [
    {"id": "web-development", "name": "Web Development", "icon": "🌐"},
    {"id": "mobile-development", "name": "Mobile Development", "icon": "📱"},
    {"id": "ui-ux-design", "name": "UI/UX Design", "icon": "🎨"},
    {"id": "backend-database", "name": "Backend/Database", "icon": "💾"},
    {"id": "ai-ml", "name": "AI/ML", "icon": "🤖"},
    {"id": "devops", "name": "DevOps", "icon": "🔧"},
    {"id": "game-development", "name": "Game Development", "icon": "🎮"},
    {"id": "security-blockchain", "name": "Security/Blockchain", "icon": "🔐"},
]


@router.get("", response_model=List[Category])
def list_categories(db: Session = Depends(get_db)) -> List[Category]:
    totals = dict(
        db.query(Question.category, func.count(Question.id))
        .filter(Question.status.in_(("published", "resolved")))
        .group_by(Question.category)
        .all()
    )

    categories: List[Category] = []
    for item in CATEGORY_SEED:
        categories.append(
            Category(
                id=item["id"],
                name=item["name"],
                icon=item.get("icon", "📁"),
                description=item.get("description", ""),
                total_questions=totals.get(item["name"], 0),
            )
        )
    return categories

