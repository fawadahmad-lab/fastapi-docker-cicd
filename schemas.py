from pydantic import BaseModel, ConfigDict




class UserCreate(BaseModel):
    email: str
    username: str 
    password: str

class UserLogin(BaseModel):
    username:str
    password:str


class TokenResponse(BaseModel):
    access_token:str
    token_type:str

class UserResponse(BaseModel):
    id: int 
    email: str
    username: str
    model_config = ConfigDict(from_attributes=True)


class TaskCreate(BaseModel):
    title: str
    description: str | None = None


class TaskUpdate(BaseModel):
    title: str
    description: str | None = None
    completed: bool


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    completed: bool

    model_config = ConfigDict(from_attributes=True)