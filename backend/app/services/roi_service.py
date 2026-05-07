from sqlalchemy.ext.asyncio import AsyncSession

from app.models.roi import ROIDetection


class ROIService:
    @staticmethod
    async def create_roi(
        db: AsyncSession,
        roi_data: dict,
    ) -> ROIDetection:
        roi = ROIDetection(**roi_data)

        db.add(roi)

        await db.commit()
        await db.refresh(roi)

        return roi
