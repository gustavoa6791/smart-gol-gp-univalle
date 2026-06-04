from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
import models
import schemas

router = APIRouter(
    prefix="/teams",
    tags=["Teams"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# category CRUD hu -005


@router.post("/categories")
def create_category(
    data: schemas.CategoryCreate,
    db: Session = Depends(get_db)
):
    exists = (
        db.query(models.Category)
        .filter(models.Category.name == data.name)
        .first()
    )

    if exists:
        raise HTTPException(
            status_code=400,
            detail="Category already exists"
        )

    category = models.Category(
        name=data.name
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


@router.get("/categories")
def get_categories(
    db: Session = Depends(get_db)
):
    return db.query(models.Category).all()


# team CRUD hu-005


@router.post("/", response_model=schemas.TeamOut)
def create_team(
    data: schemas.TeamCreate,
    db: Session = Depends(get_db)
):
    # Validar categoría

    category = (
        db.query(models.Category)
        .filter(
            models.Category.id == data.category_id
        )
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    # Validar torneo

    tournament = (
        db.query(models.Tournament)
        .filter(
            models.Tournament.id == data.tournament_id
        )
        .first()
    )

    if not tournament:
        raise HTTPException(
            status_code=404,
            detail="Tournament not found"
        )

    # Validar nombre único dentro del torneo

    existing = (
        db.query(models.Team)
        .filter(
            models.Team.name == data.name,
            models.Team.tournament_id == data.tournament_id,
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Team name already exists in tournament"
        )

    # Crear equipo

    team = models.Team(
        name=data.name,
        tournament_id=data.tournament_id,
        category_id=data.category_id,
    )

    db.add(team)
    db.commit()
    db.refresh(team)

    return team


@router.get("/", response_model=list[schemas.TeamOut])
def get_teams(
    db: Session = Depends(get_db)
):
    return db.query(models.Team).all()


@router.get("/{team_id}", response_model=schemas.TeamOut)
def get_team(
    team_id: int,
    db: Session = Depends(get_db)
):
    team = (
        db.query(models.Team)
        .filter(models.Team.id == team_id)
        .first()
    )

    if not team:
        raise HTTPException(
            status_code=404,
            detail="Team not found"
        )

    return team


@router.put("/{team_id}", response_model=schemas.TeamOut)
def update_team(
    team_id: int,
    data: schemas.TeamCreate,
    db: Session = Depends(get_db)
):
    # Verificar que el equipo exista

    team = (
        db.query(models.Team)
        .filter(models.Team.id == team_id)
        .first()
    )

    if not team:
        raise HTTPException(
            status_code=404,
            detail="Team not found"
        )

    # Validar categoría

    category = (
        db.query(models.Category)
        .filter(
            models.Category.id == data.category_id
        )
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    # Validar torneo

    tournament = (
        db.query(models.Tournament)
        .filter(
            models.Tournament.id == data.tournament_id
        )
        .first()
    )

    if not tournament:
        raise HTTPException(
            status_code=404,
            detail="Tournament not found"
        )

    # Validar nombre único dentro del torneo

    duplicate = (
        db.query(models.Team)
        .filter(
            models.Team.name == data.name,
            models.Team.tournament_id == data.tournament_id,
            models.Team.id != team_id,
        )
        .first()
    )

    if duplicate:
        raise HTTPException(
            status_code=400,
            detail="Team name already exists in tournament"
        )

    # Actualizar equipo

    team.name = data.name
    team.tournament_id = data.tournament_id
    team.category_id = data.category_id

    db.commit()
    db.refresh(team)

    return team


@router.delete("/{team_id}")
def delete_team(
    team_id: int,
    db: Session = Depends(get_db)
):
    team = (
        db.query(models.Team)
        .filter(models.Team.id == team_id)
        .first()
    )

    if not team:
        raise HTTPException(
            status_code=404,
            detail="Team not found"
        )

    db.delete(team)
    db.commit()

    return {
        "message": "Deleted successfully"
    }