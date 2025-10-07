from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_async_session
from app.models.item import Item
from app.models.order import Order, OrderItem
from app.schemas.item import ItemAdd, ItemResponse
from app.schemas.order import OrderResponse

router = APIRouter()


@router.post(
    "/{order_id}/items",
    summary="Add items to order",
    response_description="Created or updated order item",
)
async def add_item_to_order(
    order_id: int,
    payload: ItemAdd,
    db: Annotated[AsyncSession, Depends(get_async_session)],
):
    order_stmt = select(Order).where(Order.id == order_id).with_for_update()
    order = await db.scalar(order_stmt)
    if order is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Order not found")

    update_item_quantity_stmt = (
        update(Item)
        .where(Item.id == payload.item_id, Item.quantity >= payload.quantity)
        .values(quantity=Item.quantity - payload.quantity)
        .returning(Item)
    )
    item = await db.scalar(update_item_quantity_stmt)
    if item is None:
        item_exists_stmt = select(Item).where(Item.id == payload.item_id)
        item_exists = await db.scalar(item_exists_stmt)
        if item_exists is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Item not found")
        else:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, "Insufficient item quantity"
            )

    order_item = await db.scalar(
        select(OrderItem)
        .where(
            OrderItem.order_id == order_id,
            OrderItem.item_id == payload.item_id,
        )
        .with_for_update()
    )
    if order_item is None:
        order_item = OrderItem(
            order_id=order_id,
            item_id=payload.item_id,
            quantity=payload.quantity,
        )
        db.add(order_item)
    else:
        order_item.quantity += payload.quantity

    await db.flush()

    refreshed_order = await db.scalar(
        select(Order)
        .where(Order.id == order_id)
        .options(
            selectinload(Order.items).selectinload(OrderItem.item),
            selectinload(Order.customer),
        )
    )
    if refreshed_order is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Order not found")

    await db.commit()

    return OrderResponse(
        id=refreshed_order.id,
        items=[
            ItemResponse(
                id=oi.item.id,
                name=oi.item.name,
                quantity=oi.quantity,
                price=oi.item.price,
            )
            for oi in refreshed_order.items
        ],
    )
