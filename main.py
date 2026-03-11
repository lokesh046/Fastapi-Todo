from fastapi import FastAPI, Depends,HTTPException
from schema import Todo as TodoSchema, TodoCreate
from sqlalchemy.orm import Session
from database import sessionlocal, Base, engine
from models import todo

Base.metadata.create_all(bind=engine)
app = FastAPI()

# Dependency for DB session
def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()


#get all data from sever 
@app.get("/todos", response_model=list[TodoSchema])
def read_todos(db: Session = Depends(get_db)):
    return db.query(todo).all()


#get data from sever for individula 
@app.get("/todos/{todo_id}",response_model= TodoSchema)
def read_single_todo(todo_id: int ,db: Session = Depends(get_db)):
    Todo = db.query(todo).filter(todo.id== todo_id).first()
    if not Todo:
        raise HTTPException(status_code=404, detail="TODO not found")
    return Todo

# post - sending data to server 
@app.post("/todos", response_model=TodoSchema)
def create(todo_data: TodoCreate, db: Session = Depends(get_db)):
    db_todo = todo(**todo_data.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


# PUT - Update Todo
@app.put("/todos/{todo_id}",response_model=TodoSchema)
def update_todo(todo_id: int, updated: TodoCreate, db: Session = Depends(get_db)):
    Todo  = db.query(todo).filter(todo.id == todo_id).first()
    if not Todo:
        raise HTTTPException(stauts_code = 404, detail="todo not found")

    for key,value in updated.dict().items():
        setattr(Todo,key, value)
    db.commit()
    db.refresh(Todo)
    return Todo

#DELETE -- delete data from sever
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    Todo = db.query(todo).filter(todo.id == todo_id).first()
    if not Todo:
        raise HTTPExecption(status_code = 404,detail="todo not found")
    db.delete(Todo)
    db.commit()
    return {"message": "Todo deleted successfully "}

    #