from fastapi import FastAPI,Depends,HTTPException
from schema import Post,PostUpdate
import models
from database import engine,session_local
import models
from sqlalchemy.orm import Session
from datetime import datetime


app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog')
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
    return {"post":post}
    
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
    
    