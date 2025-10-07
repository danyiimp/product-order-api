from pydantic import BaseModel, ConfigDict, Field


class ItemAdd(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    item_id: int = Field(alias="id", gt=0)
    quantity: int = Field(1, gt=0)


class ItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    item_id: int = Field(alias="id", gt=0)
    name: str
    quantity: int
    price: float
