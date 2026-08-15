from fastapi import FastAPI , Depends , HTTPException
from database import engine , Base , get_db
from schemas import (
    TaskCreate ,
    TaskUpdate, 
    TaskResponse, 
    UserCreate, 
    UserResponse, 
    UserLogin, 
    TokenResponse
)
from auth import hash_password , verify_password
from security import create_access_token , get_current_user
from fastapi.security import OAuth2PasswordRequestForm

import models
from sqlalchemy.orm import Session

app = FastAPI()
Base.metadata.create_all(bind=engine)


@app.post("/auth/login",response_model=TokenResponse)
def login(form_data:OAuth2PasswordRequestForm=Depends(), db:Session = Depends(get_db)):
    user = (
        db.query(models.User).filter(models.User.username==form_data.username).first()
    )
    if user is None or not verify_password:
        form_data.password,
        user.hashed_password,
    

        raise HTTPException(status_code=401,detail="Invalid username or password")

    access_token = create_access_token(
        data={"sub": str(user.id)}

    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }




@app.post("/auth/signup", response_model=UserResponse,status_code=201)
def signup(user_data: UserCreate, db : Session = Depends(get_db)):
    existing_user = (
        db.query(models.User).filter(
            (models.User.email == user_data.email)
            | (models.User.username == user_data.username)
        ).first()
    )
    if existing_user:
        raise HTTPException(status_code=409,detail="Email or username already registered")
    
    new_user = models.User(
        email = user_data.email,
        username = user_data.username,
        hashed_password = hash_password(user_data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    
@app.get("/health")
def health_check():
    return {"status": "healthy"}




@app.get("/tasks",response_model=list[TaskResponse])
def get_tasks(db:Session=Depends(get_db),current_user: models.User = Depends(get_current_user),
    ):
    tasks=(db.query(models.Task).filter(models.Task.user_id == current_user.id).all())
    return tasks



@app.get("/tasks/{task_id}",response_model=(TaskResponse))
def get_task_by_id(
    task_id: int, db:Session=Depends(get_db),
    current_user:models.User=Depends(get_current_user)
    ):
    
    tasks=db.query(models.Task).filter(
        models.Task.id==task_id,
        models.Task.user_id== current_user.id).first()
    if tasks is None:
        raise HTTPException(status_code=404,detail='Task Not Found!')

        
    return tasks



@app.post("/tasks",response_model=TaskResponse)
def create_task(task:TaskCreate,db: Session = Depends(get_db),
                current_user: models.User=Depends(get_current_user)):
    
    new_task=models.Task(title=task.title,description=task.description,user_id=current_user.id)

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task




@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int,
                task_data: TaskUpdate,  
                db: Session=Depends(get_db),
                current_user: models.User=Depends(get_current_user)):
    
    task=db.query(models.Task).filter(models.Task.id==task_id,
                                    models.Task.user_id==current_user.id).first()
    if task is None:
        raise HTTPException(status_code=404,detail="Task Not Found! ")
        
    
    task.title=task_data.title
    task.description=task_data.description
    task.completed=task_data.completed


    db.commit()
    db.refresh(task)
    return task



@app.delete("/tasks/{task_id}")
def delete_task(task_id:int,
                db:Session=Depends(get_db),
                current_user:models.User=Depends(get_current_user)):
    
    task = db.query(models.Task).filter(models.Task.id==task_id, models.Task.user_id==current_user.id).first()
    if task is None:
        raise HTTPException(status_code=404,detail='Task Not Found!')

    

    db.delete(task)
    db.commit()
    return {"message": "Task Deleted Successfully ! "}



