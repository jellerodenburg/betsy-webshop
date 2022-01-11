from models import Asset, User, Tag, Transaction, Product, ProductTag, db
from user_data import users
from product_data import products
from tag_data import tags


def insert_data():

    with db.atomic():

        User.insert_many(
            users,
            fields=[
                User.first_name,
                User.last_name,
                User.street,
                User.house_number,
                User.house_number_addition,
                User.postal_code,
                User.city,
                User.email,
                User.telephone,
            ],
        ).execute()

        Tag.insert_many(tags).execute()

        Product.insert_many(
            products,
            fields=[
                Product.name,
                Product.description,
                Product.price_per_unit_in_cents,
            ],
        ).execute()


def create_assets():
    # get users
    alfred = User.get_by_id(1)
    barry = User.get_by_id(2)
    cornelis = User.get_by_id(3)

    # get products
    print = Product.get_by_id(1)
    statue = Product.get_by_id(2)
    bracelet = Product.get_by_id(3)

    # link users to products
    Asset.create(owner=alfred, product=print, product_quantity=5)
    Asset.create(owner=alfred, product=bracelet, product_quantity=3)
    Asset.create(owner=barry, product=statue, product_quantity=1)
    Asset.create(owner=cornelis, product=bracelet, product_quantity=3)