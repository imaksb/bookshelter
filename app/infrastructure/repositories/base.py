from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_one(self, data):
        model_obj = self.model(**data)
        self.session.add(model_obj)
        await self.session.commit()
