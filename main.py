from fastapi import FastAPI,Depends,HTTPException
from schema import Post,PostUpdate,UserCreate
import models
from database import engine,session_local
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi.security import HTTPBasic,HTTPBasicCredentials
from jose import jwt,JWTError
from dotenv import load_dotenv
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
import os
from datetime import timedelta
import secrets


pwd_context = CryptContext(schemes=['bcrypt'],deprecated='auto')

auth_scheme  = OAuth2PasswordBearer(tokenUrl='token')

load_dotenv()

SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


def get_user(username:str,db:Session = Depends(get_db)):
    return db.query(models.User).filter(models.User.username==username).first()

def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

def get_hash_password(password):
    return pwd_context.hash(password)


def create_access_token(data:dict,expiry:timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expiry
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,ALGORITHM)
    return encoded_jwt


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


@app.post('/login')
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print(form_data)
    user = get_user(username=form_data.username, db=db)
    if not user:
        raise HTTPException(404, detail="User Not Found")
    if not verify_password(form_data.password, user.password):
        raise HTTPException(400, detail="Cannot Verify Password")
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(data={"sub": user.username}, expiry=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

## create a user
@app.post('/user')
def create_user(user:UserCreate,db:Session=Depends(get_db)):
    new_user = models.User(username=user.username,password=get_hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user 



@app.post('/posts')
def create(request:Post,db:Session=Depends(get_db)):
    new_post = models.Post(title=request.title,content=request.content,created_at=request.created_at)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get('/posts')
def all_posts(db:Session=Depends(get_db)):
    posts = db.query(models.Post).all()
    return {'posts':posts}

@app.delete('/blog/{blog_id}')
def delete_post(blog_id:int,db:Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id==blog_id).first()

    if not post:
        raise HTTPException(status_code=404,detail="Post Not Found")
    
    db.delete(post)
    db.commit()

    return {"message":"post deleted"}

@app.get('/post/{post_id}')
def get_post(post_id:int,db:Session=Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id==post_id).first()

    if not post:
        raise HTTPException(status_code=404,detail="Post Not Found")
    return post
    
@app.put('/posts/{post_id}')
def update_post(post_id:int,post:PostUpdate,db:Session=Depends(get_db)):
    existing_post = db.query(models.Post).filter(models.Post.id==post_id).first()

    if not existing_post:
        raise HTTPException(status_code=404,detail="Post Not Found")
    
    existing_post.title = post.title
    existing_post.content = post.content
    existing_post.updated_at = datetime.utcnow()    
    db.commit()
    db.refresh(existing_post)
    return {"updated_post":existing_post}
    
    