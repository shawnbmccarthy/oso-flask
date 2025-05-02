from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, ForeignKey, Table

class Base(DeclarativeBase):
    ...

product_category_table = Table(
    "product_categories",
    Base.metadata,
    Column("product_id", ForeignKey("products.id"), primary_key=True),
    Column("category_id", ForeignKey("categories.id"), primary_key=True),
)

product_tag_table = Table(
    "product_tags",
    Base.metadata,
    Column("product_id", ForeignKey("products.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)

shop_employee_table = Table(
"shop_employees",
Base.metadata,
Column("shop_id", ForeignKey("shops.id"), primary_key=True),
Column("user_id", ForeignKey("users.id"), primary_key=True),
)