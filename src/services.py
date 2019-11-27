from db import ProductCatalogDB
from models import Category, Product, ProductImage
import models as Models

class ProductCatalogService():
    db = None
    def __init__(self):
        self.db = ProductCatalogDB()

    # PRODUCT METHODS
    def create_product(self, product_json):
        return ''

    def get_product(self, product_id):
        return ''

    def get_all_products(self):
        return ''

    def update_product(self, product_id, product_json):
        return ''

    def delete_product(self, product_id):
        return ''

    # CATEGORY METHODS
    def create_category(self, category_json):
        name = category_json.get('name')
        result = self.db.create_category(name)
        if (result < 0):
            return {}
        else:
            # todo get products
            new_category = Category(result, name, [])
            return new_category.to_json()

    def get_category(self, category_id):
        category = self.db.get_category_by_id(category_id)
        return category

    def get_all_categories(self):
        categories = self.db.get_all_categories()
        return categories

    def update_category(self, category_id, category_json):
        return ''

    def delete_category(self, category_id):
        return ''

    # IMAGE METHODS
    def create_image(self, image_binary):
        return ''

    