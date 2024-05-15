import boto3
from fastapi import File, UploadFile
from pydantic import UUID4

from gaming_progression_api.services.unitofwork import IUnitOfWork
from gaming_progression_api.settings import get_settings

settings = get_settings()


class PicturesService:
    async def add_picture(self, uow: IUnitOfWork, author_id: UUID4, item_id: UUID4, file: UploadFile = File(...)):
        session = boto3.session.Session()

        s3_client = session.client(
            service_name='s3',
            endpoint_url='https://hb.vkcs.cloud',
            aws_access_key_id=settings.s3_id,
            aws_secret_access_key=settings.s3_key,
            region_name='ru-msk',
        )

        s3_client.upload_fileobj(file.file, 'mbrw', file.filename, ExtraArgs={'ACL': 'public-read'})

        async with uow:
            await uow.pictures.add_one(
                {'author_id': author_id, 'item_id': item_id, 'picture_path': 'http://pictures.mbrw.ru/' + file.filename}
            )
            await uow.commit()
