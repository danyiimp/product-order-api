from pydantic import BaseModel, ConfigDict, Field

from app.schemas.item import ItemResponse


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_id: int = Field(alias="id", gt=0)
    items: list[ItemResponse]
