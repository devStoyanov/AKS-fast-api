from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from . import models, schemas
from . import utils


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def update_item(db: Session, item: schemas.ItemBase, item_id: int, user_id: int):
    item_query = db.query(models.Item).filter(models.Item.id == item_id)
    item_fetch = item_query.first()
    if item_fetch is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found",
        )
    if item_fetch.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Insufficient privileges"
        )

    item_query.update(item.dict())
    db.commit()
    db.refresh(item_fetch)
    return item_query.first()


def create_user(db: Session, user: schemas.UserCreate):
    db_check = get_user_by_email(db, email=user.email)
    if db_check:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
        )
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(
    db: Session,
    user_id: int,
):
    db_items = db.query(models.Item).filter(models.Item.owner_id == user_id)
    db_fetch = db_items.all()
    if len(db_fetch) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No items")
    return db_fetch


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, user_id: int, item_id: int):
    item_query = db.query(models.Item).filter(models.Item.id == item_id)
    item_fetch = item_query.first()
    if item_fetch == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No items")
    if item_fetch.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Insufficient privileges"
        )

    item_query.delete()
    db.commit()
