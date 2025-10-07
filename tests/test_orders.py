import asyncio

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Customer, Order
from app.models.category import Category
from app.models.item import Item
from app.schemas.item import ItemAdd


@pytest.fixture
async def customer(db):
    customer = Customer(name="John Doe")
    db.add(customer)
    await db.commit()
    return customer


@pytest.fixture
async def category(db):
    category = Category(name="Sample Category")
    db.add(category)
    await db.commit()
    return category


async def create_item(
    db: AsyncSession,
    category_id: int,
    name: str,
    quantity: int,
    price: float,
):
    item = Item(
        name=name, quantity=quantity, price=price, category_id=category_id
    )
    db.add(item)
    await db.commit()
    return item


@pytest.fixture
async def item(db, category):
    item = await create_item(
        db,
        name="Sample Item",
        quantity=1,
        price=9.99,
        category_id=category.id,
    )
    return item


@pytest.fixture
async def order(db, customer):
    order = Order(customer_id=customer.id)
    db.add(order)
    await db.commit()
    return order


async def test_add_item_to_order(order, item, ac):
    response = await ac.post(
        f"/orders/{order.id}/items",
        json=ItemAdd.model_validate(item).model_dump(by_alias=True),
    )
    assert response.status_code == 200, response.text


async def test_add_item_when_insufficient_quantity(order, item, ac):
    response = await ac.post(
        f"/orders/{order.id}/items",
        json=ItemAdd.model_validate(item).model_dump(by_alias=True)
        | {"quantity": 10},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Insufficient item quantity"


async def test_add_item_to_nonexistent_order(item, ac):
    nonexistent_order_id = 1
    response = await ac.post(
        f"/orders/{nonexistent_order_id}/items",
        json=ItemAdd.model_validate(item).model_dump(by_alias=True),
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found"


async def test_add_nonexistent_item_to_order(order, ac):
    nonexistent_item_id = 1
    response = await ac.post(
        f"/orders/{order.id}/items",
        json={"id": nonexistent_item_id, "quantity": 1},
    )
    assert response.status_code == 404, response.text
    assert response.json()["detail"] == "Item not found"


async def test_concurrent_add_item_to_order(order, item, ac):
    async def add_item():
        response = await ac.post(
            f"/orders/{order.id}/items",
            json=ItemAdd.model_validate(item).model_dump(by_alias=True),
        )
        return response

    tasks = [add_item() for _ in range(5)]
    responses = await asyncio.gather(*tasks)

    success_count = sum(1 for r in responses if r.status_code == 200)
    failure_count = sum(1 for r in responses if r.status_code == 400)

    assert success_count == 1, f"Expected 1 success, got {success_count}"
    assert failure_count == 4, f"Expected 4 failures, got {failure_count}"

    for r in responses:
        if r.status_code == 400:
            assert r.json()["detail"] == "Insufficient item quantity"


async def test_double_add_item(order, category, ac, db):
    item = await create_item(db, category.id, category.name, 5, 19.99)

    async def add_item():
        response = await ac.post(
            f"/orders/{order.id}/items",
            json=ItemAdd(id=item.id, quantity=1).model_dump(by_alias=True),
        )
        return response

    response = await add_item()
    assert response.status_code == 200, response.text
    assert response.json()["items"][0]["quantity"] == 1

    response = await add_item()
    assert response.status_code == 200, response.text
    assert response.json()["items"][0]["quantity"] == 2
