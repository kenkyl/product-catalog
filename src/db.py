import redis
import models as Models

# REDIS CONSTANTS
redis_host = 'localhost'
redis_port = 6379
# NAMESPACE CONSTANTS
category_id_key = 'categoryid'
categories_key = 'categories'
product_id_key = 'productid'
products_categories_map_key = 'products'

class ProductCatalogDB():
    r = None
    def __init__(self):
        self.r = redis.Redis(host=redis_host, port=redis_port)
    
    def create_category(self, category_name):
        category_id = self.r.incr(category_id_key)
        print(f'new category id = {category_id}, name={category_name}')
        value = self.r.zadd(categories_key, {category_name: float(category_id)})
        if (value > 0):
            return category_id
        else:
            return -1

    def get_all_categories(self):
        category_list = self.r.zrangebyscore(categories_key, '-inf', '+inf', withscores=True)
        print(f'got categories: {category_list}')
        category_dict = dict(category_list)
        # convert key byte values to strings
        category_dict = { y.decode('ascii'): int(category_dict.get(y)) for y in category_dict.keys() }
        print(f'ret categories: {category_dict}')
        return category_dict

    def get_category_by_id(self, category_id):
        category_list = self.r.zrangebyscore(categories_key, category_id, category_id, start=0, num=1)
        print(f'got categories: {category_list}')
        value = category_list[0] if(len(category_list) > 0) else ''
        return value

    def create_product(self, product_json):
        # 1. check category 
        category = product_json.get('category')
        category_id = 0
        if (category):
            category_id = category.get('id')
            if (self.get_category_by_id(category_id) == ''):
                # return if category does not exist
                return -1                
        else:
            return -1
        # 2. get id 
        product_id = self.r.incr(product_id_key)
        product_id_str = f'products:{product_id}'
        product_value = {
            'id': product_id,
            'name': product_json.get('name'),
            'description': product_json.get('description'),
            'vendor': product_json.get('vendor'),
            'price': product_json.get('price'),
            'currency': product_json.get('currency'),
            'category': str(product_json.get('category')),
            'images': str(product_json.get('images'))    
        }
        # 3. add to product sorted set
        self.r.zadd(products_categories_map_key, {str(product_value): float(category_id)})
        # 4. add product hash
        # TODO - decide if and where to split out images
        value = self.r.hmset(product_id_str, product_value)
        if (value > 0):
            return product_id
        else:
            return -1

    def get_product_by_id(self, product_id):
        product_value = self.r.hgetall(product_id)
        print(f'got product: {product_value}')
        if (product_value):
            product_value = { y.decode('ascii'): product_value.get(y).decode('ascii') for y in product_value.keys() }
        return product_value

    def search_products_by_name(self, search_term):
        return ''

    def search_products_by_category_id(self, category_id):
        products = self.r.zrangebyscore(products_categories_map_key, category_id, category_id)
        print(f'got products: {products}')
        if (products):
            products = [ y.decode('ascii') for y in products ]
        return products

