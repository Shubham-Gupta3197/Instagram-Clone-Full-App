import random
import string
from typing import List
import datetime
import os

from db.repository.posts import create_post, get_all_posts
from db.session import get_db
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from schemas.post import PostShow, PostCreate
from sqlalchemy.orm import Session

router = APIRouter()

img_url_types = ['absolute', 'relative']


def get_unique_random_name():
    letters = string.ascii_letters
    time = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
    rand_str = ''.join(random.choice(letters) for n in range(7))
    tmp_name = time + rand_str
    if not os.path.isfile(f'./images/{tmp_name}'):
        return tmp_name
    return get_unique_random_name()


@router.post("/create", response_model=PostShow)
def create_new_post(given_post: PostCreate, db: Session = Depends(get_db)):
    if not given_post.img_url_type in img_url_types:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Image url type can only be: ""Absolute / Relative.")
    return create_post(given_post=given_post, db=db)


@router.post("/image")
def upload_image(image: UploadFile = File(...)):
    allowed_formats = ['.png', '.jpg', 'jpeg', '.png', '.bmp']
    format_file = image.filename[image.filename.rfind('.'):].lower()
    if format_file in allowed_formats:
        unique_name = get_unique_random_name() + format_file
        path = f'./images/{unique_name}'
        with open(path, "w+b") as file_object:
            file_object.write(image.file.read())
        return {"detail": "succeed", "path": path}
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        detail="Images formats must be: png/jpg/jpeg/bmp")


@router.get("/all", response_model=List[PostShow])
def get_all(db: Session = Depends(get_db)):
    return get_all_posts(db)