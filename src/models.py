class ProductImage:
    def __init__(self, imageId, value):
        self.id = imageId 
        self.value = value


class Product:
    product_id = ''
    name = ''
    description = ''
    vendor = ''
    price = ''
    currency = ''
    category = ''
    images = []

    def __init__(self, product_json):
        keys = product_json.keys()
        self.name = product_json.get('name') if('name' in keys) else 'new product'
        self.description = product_json.get('description') if('description' in keys) else 'a lovely product'
        self.vendor = product_json.get('vendor') if('vendor' in keys) else 'wally world'
        self.price = product_json.get('price') if('price' in keys) else '100'
        self.currency = product_json.get('currency') if('currency' in keys) else 'usd'
        self.category = product_json.get('category') if('category' in keys) else 'category'
        if ('images' in keys and (len(product_json.get('images')) > 0)):
            # TODO - figure out where to separate picture creation
            self.images = product_json.get('images')
            #for image in images:



class Category:
    categoryId = 0
    name = ''
    products = []

    def __init__(self, categoryId, name, products):
        self.categoryId = categoryId
        self.name = name
        self.products = products

    def to_json(self):
        return {
            'id': self.categoryId,
            'name': self.name,
            'products': self.products
        }
