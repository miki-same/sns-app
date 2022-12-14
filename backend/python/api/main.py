from cgitb import handler
from fastapi import FastAPI, File, UploadFile
from routers import users,posts,likes,follow,search,security
import shutil
import os
from mangum import Mangum
from setting import Settings
from fastapi.middleware.cors import CORSMiddleware

settings=Settings()

if settings.CONFIG=='production':
    app=FastAPI(
        openapi_url='/openapi.json',
        root_path="/dev/" #api gatewayのstage名に合わせる Swagger UI利用のため
        )   
else:
    app=FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(likes.router)
app.include_router(follow.router)
app.include_router(search.router)
app.include_router(security.router)

@app.get("/hello")
def hello():
    return {"message": "hello world!"}

UPLOAD_DIR = "./static/img"

@app.post("/file_upload")
def file_upload(file: UploadFile = File(None)):
    if file:
        filename=file.filename
        fileobj=file.file
        
        with open(UPLOAD_DIR+f'/{filename}', 'w+b') as upload_dir:
            shutil.copyfileobj(fileobj,upload_dir)

        return {
            "filename":file.filename
        }
    
    return {"Detail": "File not uploaded"}