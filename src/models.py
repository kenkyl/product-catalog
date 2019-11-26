class ProductImage:
    def __init__(self, imageId, value):
        self.id = imageId 
        self.value = value


class Product:
    def __init__(self, productId, name, description, vendor, price, currency, mainCategory, images):
        self.productId = productId
        self.name = name
        self.description = description
        self.vendor = vendor
        self.price = price
        self.currency = currency
        self.mainCategory = mainCategory
        self.images = images


class Category:
    def __init__(self, categoryId, name, products):
        self.categoryId = categoryId
        self.name = name
        self.products = products
