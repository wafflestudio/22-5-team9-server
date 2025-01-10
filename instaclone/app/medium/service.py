import boto3
import os
from uuid import uuid4
from typing import Annotated, List, Sequence
from fastapi import Depends, HTTPException, UploadFile
from sqlalchemy.sql import select

from instaclone.database.connection import SESSION
from instaclone.app.medium.store import MediumStore
from instaclone.app.medium.models import Medium
from instaclone.app.post.models import Post
from instaclone.app.medium.errors import FileSizeLimitError, FailedToSave

MAX_FILE_SIZE = 10 * 1024 * 1024
BASE_DIR = "media_uploads"

class MediumService:
    def __init__(self, medium_store: Annotated[MediumStore, Depends()]) -> None:
        self.medium_store = medium_store
        self.upload_folder = "Post uploads"  

        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder)

        # Make S3 client
        #self.s3_client = boto3.client(
        #    "s3",
        #    aws_access_key_id="your-access-key",
        #    aws_secret_access_key="your-secret-key",
        #    region_name="your-region",
        #)
        #self.s3_client = boto3.client("s3")
        #self.bucket_name = "your-s3-bucket-name"

    async def save_file_locally(self, file: UploadFile) -> str:
        """
        Save the uploaded file to the local directory and return its path.
        """
        try:
            if file.filename:
                file_path = os.path.join(self.upload_folder, file.filename)
            else:
                raise FailedToSave()

            with open(file_path, "wb") as f:
                while content := await file.read(1024):  # Read file in chunks
                    f.write(content)

            return file_path
        except Exception as e:
            raise FailedToSave()

    # async def upload_image_to_s3(self, file: UploadFile) -> str:
    #     try:
    #         file_extension = file.filename.split(".")[-1]
    #         file_key = f"media/{uuid4()}.{file_extension}"

    #         # Upload file to S3
    #         self.s3_client.upload_fileobj(
    #             file.file,
    #             self.bucket_name,
    #             file_key,
    #             ExtraArgs={"ACL": "public-read", "ContentType": file.content_type},
    #         )

    #         return f"https://{self.bucket_name}.s3.amazonaws.com/{file_key}"
    #     except Exception as e:
    #         raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")

    '''async def create_medium(self, post_id: int | None, 
                            #story_id: int | None, 
                            file: UploadFile) -> Medium:
        url = await self.upload_image_to_s3(file)

        file_name = file.filename
        return await self.medium_store.add_medium(post_id=post_id, 
                                                  #story_id=story_id, 
                                                  file_name=file_name, url=url)

    async def get_medium(self, image_id: int) -> Medium:
        medium = await self.medium_store.get_medium_by_id(image_id)
        if not medium:
            raise ValueError("Medium not found.")
        return medium

    async def get_media_by_post(self, post_id: int) -> List[Medium]:
        return await self.medium_store.get_media_by_post(post_id)

    #async def get_media_by_story(self, story_id: int) -> List[Medium]:
    #    return await self.medium_store.get_media_by_story(story_id)

    async def delete_medium(self, image_id: int) -> None:
        await self.medium_store.delete_medium(image_id) ''' 
    
    async def create_medium(self, post_id: int | None, 
                            story_id: int | None, 
                            file: UploadFile) -> Medium:
        if file.filename == None:
            raise FailedToSave()
        
        if post_id:
            post = await SESSION.scalar(select(Post).where(Post.post_id == post_id))
            if not post:
                raise HTTPException(status_code=400, detail="Invalid post_id. No corresponding post found.")
        # Save file locally
        file_path = await self.save_file_locally(file)

        return await self.medium_store.add_medium(
            post_id=post_id,
            # story_id=story_id,
            file_name=file.filename,
            url=file_path,  
        )

    async def get_medium(self, image_id: int) -> Medium:
        medium = await self.medium_store.get_medium_by_id(image_id)
        if not medium:
            raise ValueError("Medium not found.")
        return medium

    async def delete_medium(self, image_id: int) -> None:
        await self.medium_store.delete_medium(image_id)
    
    async def get_media_by_post(self, post_id: int) -> Sequence[Medium]:
        return await self.medium_store.get_media_by_post(post_id)
    
    async def file_to_medium(self, file: UploadFile) -> Medium:
        """
        파일을 저장하고 medium을 생성합니다.
        """
        if len(await file.read()) > MAX_FILE_SIZE:
            raise FileSizeLimitError()

        await file.seek(0)

        unique_filename = f"{uuid4().hex}_{file.filename}"
        file_path = os.path.join(BASE_DIR, unique_filename)
        
        os.makedirs(BASE_DIR, exist_ok=True)

        with open(file_path, "wb") as buffer:
            while content := await file.read(1024):
                buffer.write(content)

        medium = await self.medium_store.add_medium(file_name=unique_filename, url=file_path, post_id=None)
        return medium

        
