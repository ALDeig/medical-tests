import sqlalchemy as sa
from sqlalchemy.orm import selectinload

from app.src.models.models import Patient
from app.src.services.db.dao import BaseDAO
from app.src.services.db.base import session_factory


class PatientDAO(BaseDAO):

    @classmethod
    async def get_patient_with_tests(
        cls, model: type[Patient], **filter_by
    ) -> Patient | None:
        query = (
            sa.select(model)
            .options(selectinload(model.medical_test))
            .filter_by(**filter_by)
        )
        async with session_factory() as session:
            response = await session.scalar(query)
            return response
            # if response is not None:
            #     print(response.medical_test)
            #     return SPatient.model_validate(response)
            # print(response.medical_test)
            # return response
