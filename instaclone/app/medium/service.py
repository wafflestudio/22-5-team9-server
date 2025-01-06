import boto3
from uuid import uuid4
from typing import Annotated, List
from fastapi import Depends, HTTPException, UploadFile
from instaclone.app.medium.store import MediumStore
from instaclone.app.medium.models import Medium


class MediumService:
    def __init__(self, medium_store: Annotated[MediumStore, Depends()]) -> None:
        self.medium_store = medium_store

        # Make S3 client
        #self.s3_client = boto3.client(
        #    "s3",
        #    aws_access_key_id="your-access-key",
        #    aws_secret_access_key="your-secret-key",
        #    region_name="your-region",
        #)
        self.s3_client = boto3.client("s3")
        self.bucket_name = "your-s3-bucket-name"

    async def upload_image_to_s3(self, file: UploadFile) -> str:
        try:
            file_extension = file.filename.split(".")[-1]
            file_key = f"media/{uuid4()}.{file_extension}"

            # Upload file to S3
            self.s3_client.upload_fileobj(
                file.file,
                self.bucket_name,
                file_key,
                ExtraArgs={"ACL": "public-read", "ContentType": file.content_type},
            )

            return f"https://{self.bucket_name}.s3.amazonaws.com/{file_key}"
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")

    async def create_medium(self, post_id: int | None, 
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
        await self.medium_store.delete_medium(image_id)
