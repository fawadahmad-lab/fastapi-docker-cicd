from pydantic import BaseModel

class TaskCreate(BaseModel):
    title:str
    description: str | None = None




class TaskUpdate(BaseModel):
    title:str
    description: str | None = None
    completed: bool

    

class TaskResponse(BaseModel):
    id: int 
    title: str 
    description: str | None = None
    completed: bool 


    class config:
        from_attributes=True



