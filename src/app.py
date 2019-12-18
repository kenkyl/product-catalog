from flask import Flask
from flask import request, jsonify, abort
from db import ProductCatalogDB
import json

# SETUP
app = Flask(__name__)

redis_db = ProductCatalogDB()

@app.route('/')
def hello_world():
    return 'Wilkommen, Leute!'

# PRODUCTS ENDPOINT
# POST  -> Create a new product 
# GET   -> Fetch all products 
@app.route('/products', methods=['POST', 'GET'])
def products_handler():
    if (request.method == 'POST'):
        # create product
        print('creating product...')
        body = request.get_json()
        create = redis_db.create_product(body)
        print(f'create val: {create}')
        if (create == -1):
            return 'error creating category', 400
        else:
            return str(create) 
    elif (request.method == 'GET'):
        # get all products
        print('fetching all products...')
        products = redis_db.get_all_products()
        print(f'got products: {products}')
        return json.dumps(products), 200, {'Content-Type':'application/json'}
    else: 
        # reject request 
        print('rejecting request')
    return 'Products endpoint reached'

# PRODUCT (ID) ENDPOINT
# GET   -> Fetch a product by id 
# PUT   -> Update a product by id
# DELETE-> Delete a product by id
@app.route('/products/<int:product_id>', methods=['GET', 'PUT', 'DELETE'])
def product_handler(product_id):
    if (request.method == 'GET'):
        # get one product
        print(f'fetching product with id {product_id}...')
        product = redis_db.get_product_by_id(f'products:{product_id}')
        if (product):
            return product, 200, {'Content-Type':'application/json'}
        else:
            abort(404)
    elif (request.method == 'PUT'):
        # update product
        print(f'updating product with id {product_id} ...')
    elif (request.method == 'DELETE'): 
        # delete product
        print(f'deleting product with id {product_id}...')
    return 'Product endpoint reached'

@app.route('/products/search-by-name/<search_term>', methods=['GET'])
def product_search_handler(search_term):
    print(f'searching for products with name containing {search_term}')
    matches = redis_db.search_products_by_name(search_term)
    return json.dumps(matches), 200, {'Content-Type':'application/json'}

@app.route('/products/search-by-category/<int:category_id>', methods=['GET'])
def product_search_by_cat_handler(category_id):
    print(f'searching for products in category with id {category_id}')
    products = redis_db.search_products_by_category_id(category_id)
    if (not products):
        abort(404)
    return json.dumps(products), 200, {'Content-Type':'application/json'}
    

# CATEGORIES ENDPOINT
# POST  -> Create a new category 
# GET   -> Fetch all categories 
@app.route('/categories', methods=['POST', 'GET'])
def categories_handler():
    if (request.method == 'POST'):
        # create categories
        print('creating category...')
        body = request.get_json()
        name = body.get('name')
        create = redis_db.create_category(name)
        print(f'create val: {create}')
        if (create == -1):
            return 'error creating category', 400
        else:
            return str(create) 
    elif (request.method == 'GET'):
        # get all categories
        print('fetching all categories...')
        categories = redis_db.get_all_categories()
        #if (categories)
        return jsonify(categories)
    else: 
        # reject request 
        print('rejecting request')
        abort(404)
    return 'Categories endpoint reached'

# CATEGORY (ID) ENDPOINT
# GET   -> Fetch a category by id 
# PUT   -> Update a category by id
# DELETE-> Delete a category by id
@app.route('/categories/<int:category_id>', methods=['GET', 'PUT', 'DELETE'])
def category_handler(category_id):
    if (request.method == 'GET'):
        # get one category
        print(f'fetching category with id {category_id}...')
        category = redis_db.get_category_by_id(category_id)
        if (category == ''): 
            abort(404)
        else:
            return category, 200, {'Content-Type':'application/json'}
    # elif (request.method == 'PUT'):
    #     # update category
    #     print(f'updating category with id {category_id} ...')
    elif (request.method == 'DELETE'): 
        # delete category
        print(f'deleting category with id {category_id}...')
    return 'Product endpoint reached'