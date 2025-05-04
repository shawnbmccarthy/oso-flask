"""

"""
from logging import Logger
from random import randrange, randint
from os import environ
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session
from typing import List
from oso_demo.models import (
    User, Shop, Product, Category, Tag,
    Cart, CartItem
)
from oso_cloud import Oso, Value

logger: Logger = Logger(__name__)

# prefixes needed for seeding
customer_prefix = "customer_"
shop_owner_prefix = "owner_"
staff_prefix = "staff_"
shop_prefix = "shop_"

def create_users(session: Session) -> None:
    logger.info("creating users, shop owners & staff")
    users: List[User] = []
    for i in range(1, 6):
        users.append(User(email=f"{customer_prefix}{i}@example.com", name=f"{customer_prefix}{i}"))

    for i in range(1, 6):
        users.append(User(email=f"{shop_owner_prefix}{i}@example.com", name=f"{shop_owner_prefix}{i}"))
        users.append(User(email=f"{staff_prefix}{i}@example.com", name=f"{staff_prefix}{i}"))

    session.add_all(users)
    session.commit()

def create_shops(session: Session, oso: Oso) -> None:
    logger.info("creating shops")
    shops: List[Shop] = []
    with session.no_autoflush:
        shop_owners = session.query(User).filter(User.name.like(f"{shop_owner_prefix}%")).all()
        for shop_owner in shop_owners:
            i: str = shop_owner.name.split("_")[1]
            staff_user = session.query(User).filter(User.name.like(f"{staff_prefix}{i}")).first()
            shops.append(Shop(
                name=f"{shop_prefix}{i}",
                description=f"{shop_owner.name} store front",
                owner=shop_owner,
                employees=[staff_user] if staff_user else []
            ))
    session.add_all(shops)
    session.commit()
    # create oso roles now that SQL commit is completed
    with oso.batch() as tx:
        for shop in shops:
            tx.insert(("has_relation", Value("Shop", shop.id), "owner", Value("User", shop.owner.id)))
            if shop.is_active:
                tx.insert(("is_active", Value("Shop", shop.id)))
            for employee in shop.employees:
                tx.insert(("has_role", Value("User", employee.id), "staff", Value("Shop", shop.id)))

def create_products(session: Session, oso: Oso) -> None:
    logger.info("creating products (5 per shop)")
    products: List[Product] = []
    for shop in session.query(Shop).all():
        for i in range(1, 6):
            p: Product = Product(
                name=f"{shop.name}_product_{i}",
                description=f"{shop.name} product {i}",
                price=float(randrange(5, 200, step=5)),
                quantity=randrange(5, 100, step=1),
                shop=shop,
            )
            products.append(p)

    session.add_all(products)
    session.commit()
    with oso.batch() as tx:
        for product in products:
            tx.insert(("has_relation", Value("Product", product.id), "belongs_to", Value("Shop", product.shop.id)))
            if product.is_active:
                tx.insert(("is_active", Value("Product", product.id)))

def create_product_categories(session: Session) -> None:
    logger.info("creating product categories")
    categories: List[Category] = []

    for i in range(1, 6):
        categories.append(Category(name = f"category_product_{i}"))

    session.add_all(categories)

    for i in range(1, 6):
        products = session.query(Product).filter(Product.name.like(f"%product_%")).all()
        category = session.query(Category).filter(Category.name.like(f"category_product_{i}")).first()

        for product in products:
            product.categories.append(category)

        session.add_all(products)
    session.commit()

def create_product_tags(session: Session) -> None:
    logger.info("creating product tags")
    tags: List[Tag] = []

    for i in range(1, 6):
        tags.append(Tag(name=f"tag_shop_{i}"))
    session.add_all(tags)

    for i in range(1, 6):
        products = session.query(Product).filter(Product.name.like(f"{shop_prefix}{i}%")).all()
        for product in products:
            t = session.query(Tag).filter(Tag.name.like(f"tag_shop_{i}")).first()
            product.tags.append(t)

        session.add_all(products)
    session.commit()

def create_cart(session: Session, user: User, is_public: bool) -> (Cart, List[CartItem]):
    with session.no_autoflush:
        no_of_items = randint(1, 3)
        cart_items_for_user = []
        c = Cart(user=user, is_public=is_public)
        for i in range(no_of_items):
            shop_id = randint(1, 5)
            prod_id = randint(1, 5)
            q = randint(1, 5)
            p = session.query(Product).filter(Product.name.like(f"{shop_prefix}{shop_id}_product_{prod_id}")).first()
            ci = CartItem(cart=c, product=p, quantity=q)
            cart_items_for_user.append(ci)
    return c, cart_items_for_user

def create_carts(session: Session, oso: Oso) -> None:
    logger.info("creating carts")
    carts: List[Cart] = []
    cart_items: List[CartItem] = []
    users = session.query(User).filter(User.name.like(f"{customer_prefix}%")).all()
    for user in users:
        c_t, ci_t = create_cart(session, user, True)
        c_f, ci_f = create_cart(session, user, False)
        carts.append(c_t)
        carts.append(c_f)
        cart_items.extend(ci_t)
        cart_items.extend(ci_f)
    session.add_all(carts)
    session.add_all(cart_items)
    session.commit()
    with oso.batch() as tx:
        for cart in carts:
            tx.insert(("has_relation", Value("Cart", cart.id), "owner", Value("User", cart.user.id)))
            if cart.is_public:
                tx.insert(("is_public", Value("Cart", cart.id)))


def main():
    db_url: str | None = environ.get("DATABASE_URL")
    if not db_url:
        raise Exception("DATABASE_URL environment variable not set")

    engine: Engine = create_engine(db_url, echo=False)
    oso: Oso = Oso(environ.get("OSO_URL"), environ.get("OSO_AUTH"), environ.get("OSO_DATA_BINDINGS") or {} )
    # clean up oso
    oso.delete(("has_relation", None, None, None))
    oso.delete(("has_role", None, None, None))
    oso.delete(("is_active", None))
    oso.delete(("is_public", None))

    with Session(engine) as session:
        logger.info("create initial shop data")
        # users:
        create_users(session)
        # shops:
        create_shops(session, oso)
        # products:
        create_products(session, oso)
        # categories & product_categories:
        create_product_categories(session)
        # tags & product_tags
        create_product_tags(session)
        # carts & cart_items
        create_carts(session, oso)
        # orders & order_items

if __name__ == "__main__":
    logger.info("starting seed of data")
    main()