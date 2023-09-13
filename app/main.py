from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from . import crud, models, schemas, oauth2
from . database import get_db, engine
from . import auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.route)


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)



@app.post("/items/", response_model=schemas.Item)
def create_item_for_user(
    item: schemas.ItemCreate, db: Session = Depends(get_db), current_user: int=Depends(
        oauth2.get_current_user)):
    
    return crud.create_user_item(db=db, item=item, user_id=current_user.id)

@app.get("/items/", response_model=list[schemas.Item])
def read_items(db: Session = Depends(get_db), current_user: int=Depends(
    oauth2.get_current_user)):
    items = crud.get_items(db, user_id=current_user.id)
    return items

@app.put("/items/{id}", response_model=schemas.Item)
def change_item(id: int ,item: schemas.ItemCreate, db: Session = Depends(get_db), current_user: int=Depends(
    oauth2.get_current_user)):
    item_updated = crud.update_item(db=db, item=item, item_id=id, user_id=current_user.id) 
    return item_updated

@app.delete("/items/{id}")
def delete_item_db(id: int, db: Session = Depends(get_db), current_user: int=(Depends(oauth2.get_current_user))):
    item = crud.delete_item(db, item_id=id, user_id=current_user.id)
    if item  == None:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Deleted")

@app.get("/users/")
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


