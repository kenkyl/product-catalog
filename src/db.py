import redis
import redisearch
import models as Models

# REDIS CONSTANTS
redis_host = 'localhost'
redis_port = 6379
# NAMESPACE CONSTANTS
category_id_key = 'categoryid'
categories_key = 'categories'
product_id_key = 'productid'
products_categories_map_key = 'products'
products_hash_key = 'products-hash'

class ProductCatalogDB():
    r = None
    rs = None
    def __init__(self):
        # setup redis clients
        self.r = redis.Redis(host=redis_host, port=redis_port)
        self.rs = redisearch.Client('product_name', host=redis_host, port=redis_port)
        try:
            self.rs.create_index((
                redisearch.NumericField('id'),
                redisearch.TextField('name'),
                redisearch.TextField('description'),
                redisearch.TextField('vendor'),
                redisearch.NumericField('price'),
                redisearch.TextField('currency'),
                redisearch.TextField('category'),
                redisearch.TextField('images')
            ))
        except Exception:
            print(f'error creating index')
        print(f'index info: {self.rs.info()}')
    
    def create_category(self, category_name):
        # REDIS - INCR
        category_id = self.r.incr(category_id_key)
        print(f'new category id = {category_id}, name={category_name}')
        # REDIS - ZADD
        # <categoryname>:<id> -> 0 (all score set to 0)
        value = self.r.zadd(categories_key, {category_name: float(category_id)})
        if (value > 0):
            return category_id
        else:
            return -1

    def get_all_categories(self):
        # REDIS - ZRANGEBYSCORE
        category_list = self.r.zrangebyscore(categories_key, '-inf', '+inf', withscores=True)
        print(f'got categories: {category_list}')
        category_dict = dict(category_list)
        # convert key byte values to strings
        category_dict = { y.decode('ascii'): int(category_dict.get(y)) for y in category_dict.keys() }
        print(f'ret categories: {category_dict}')
        return category_dict

    def get_category_by_id(self, category_id):
        # REDIS - ZRANGEBYSCORE
        # currently only useful if you know the ID 
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
        # REDIS - INCR
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
        # REDIS - ZADD
        # currently would have to know 
        self.r.zadd(products_categories_map_key, {product_id_str: float(category_id)})

        # NEW - add product to hash 
        product_name_str = str.lower(product_json.get('name')).replace(' ', '')
        self.r.hset(f'{products_categories_map_key}:lookup', product_name_str, product_id_str)

        # 4. add product hash
        # TODO - decide if and where to split out images
        # REDISEARCH - ADD 
        index_value = self.rs.add_document(
            product_id_str,
            id=product_id,
            name=product_json.get('name'),
            description=product_json.get('description'),
            vendor=product_json.get('vendor'),
            price=product_json.get('price'),
            currency=product_json.get('currency'),
            category=str(product_json.get('category')),
            images=str(product_json.get('images'))
        )
        print(f'index add document result: {index_value}')
        # REDIS - HMSET
        value = self.r.hmset(product_id_str, product_value)
        if (value > 0):
            return product_id
        else:
            return -1

    def get_all_products(self):
        products = []
        idx = 0
        while (True):
            # REDIS - SCAN
            products_scan = self.r.scan(idx, match="products:*")
            print(f'products scan got: {products_scan}')
            if (products_scan[1]):
                for y in products_scan[1]:
                    products.append(y.decode('ascii'))
            if (products_scan[0] == 0):
                break
            idx = products_scan[0]
        if (products):
            # loop through and grab product info for each
            products = [ self.get_product_by_id(y) for y in products ]
        return products

    def get_product_by_id(self, product_id):
        # REDIS - HGETALL
        product_value = self.r.hgetall(product_id)
        print(f'got product: {product_value}')
        if (product_value):
            product_value = { y.decode('ascii'): product_value.get(y).decode('ascii') for y in product_value.keys() }
        return product_value

    # method 1 - hscan 
    def search_products_by_name(self, search_term):
        # 1.a. scan keys for all products (SCAN 0 MATCH products:*)
        match_string = str.lower(search_term.replace(' ', ''))
        num, products_matches = self.r.hscan(f'{products_categories_map_key}:lookup', match=match_string)
        print(products_matches)
        product = {}
        if (products_matches):
            product_id = products_matches.get(next(iter(products_matches))).decode('ascii')
            product = self.get_product_by_id(product_id)
            #products_matches = { y.decode('ascii'): products_matches.get(y).decode('ascii') for y in products_matches.keys() }
        return product
        
    # method 2 - redisearch
    def rsearch_products_by_name(self, search_term):
        # method 1 - scan 
        # 1.a. scan keys for all products (SCAN 0 MATCH products:*)
        products_search = self.rs.search(search_term)
        products = []
        print(f'Redisearch products total: {products_search.total}')
        print(f'Redisearch products: {products_search.docs}')
        for doc in products_search.docs:
            products.append(doc.__dict__)
        return products

    def search_products_by_category_id(self, category_id):
        # REDIS - ZRANGEBYSCORE
        products = self.r.zrangebyscore(products_categories_map_key, category_id, category_id)
        print(f'got products: {products}')
        if (products):
            # loop through and grab product info for each
            products = [ self.get_product_by_id(y.decode('ascii')) for y in products ]
        return products