import redis
import models as Models

# REDIS CONSTANTS
redis_host = 'localhost'
redis_port = 6379
# NAMESPACE CONSTANTS
category_id_key = 'categoryid'
categories_key = 'categories'

class ProductCatalogDB():
    r = None
    def __init__(self):
        self.r = redis.Redis(host=redis_host, port=redis_port)
    
    def create_category(self, category_name):
        category_id = self.r.incr(category_id_key)
        print(f'new category id = {category_id}, name={category_name}')
        value = self.r.zadd(categories_key, {category_name: category_id})
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
