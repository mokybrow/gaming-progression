from fastapi import HTTPException, status

from gaming_progression_api.models.service import CreateReportModel
from gaming_progression_api.services.unitofwork import IUnitOfWork
from gaming_progression_api.settings import get_settings

settings = get_settings()


class ReportsService:
   async def create_report(self, uow: IUnitOfWork, user_id, report: CreateReportModel):
        async with uow:
            unique_report = await uow.reports.find_one(user_id=user_id, content_id=report.content_id)
            if unique_report:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="You already report this content",
                )
            await uow.reports.add_one({'user_id': user_id, 
                                       'type': report.type, 
                                       'content_id': report.content_id, 
                                       'content_type': report.content_type, 
                                       'description': report.description})
            
            await uow.commit()
               