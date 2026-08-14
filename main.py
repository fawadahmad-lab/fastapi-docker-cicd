from fastapi import FastAPI , Depends , HTTPException
from database import engine , Base , get_db
from schemas import TaskCreate , TaskUpdate, TaskResponse
import models
# from sqlalchemy.orm import Session

from sqlalchemy.orm import Session



app = FastAPI()





@app.get("/health")
def health_check():
    return {"status": "healthy"}


Base.metadata.create_all(bind=engine)

@app.get("/tasks",response_model=list[TaskResponse])
def get_tasks(db:Session=Depends(get_db)):
    tasks=db.query(models.Task).all()
    return tasks



@app.get("/tasks/{task_id}",response_model=(TaskResponse))
def get_task_by_id(task_id: int, db:Session=Depends(get_db)):
    tasks=db.query(models.Task).filter(models.Task.id==task_id).first()
    if tasks is None:
        raise HTTPException(status_code=404,detail='Task Not Found!')

        
    return tasks



# @app.get("/test-db")
# def test_db():
#     try:
#         with engine.connect() as connection:
#             return {"database": "connected!"}
#     except Exception as e:
#         return {"database":"connection failed!", "error": str(e)}

#TEST ENDPOINT - temp

# @app.post("/task-create")
# def create_task(task: TaskCreate):
#     return task



@app.post("/tasks",response_model=TaskResponse)
def create_task(task:TaskCreate,db: Session = Depends(get_db)):
    new_task=models.Task(title=task.title,description=task.description)

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task




@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_data: TaskUpdate,  db: Session=Depends(get_db)):
    task=db.query(models.Task).filter(models.Task.id==task_id).first()
    if task is None:
        raise HTTPException(status_code=404,detail="Task Not Found! ")
        
    
    task.title=task_data.title
    task.description=task_data.description
    task.completed=task_data.completed


    db.commit()
    db.refresh(task)
    return task



@app.delete("/tasks/{task_id}")
def delete_task(task_id:int,db:Session=Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id==task_id).first()
    if task is None:
        raise HTTPException(status_code=404,detail='Task Not Found!')

    

    db.delete(task)
    db.commit()
    return {"message": "Task Deleted Successfully ! "}



