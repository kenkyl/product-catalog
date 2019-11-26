from flask import Flask
from flask import request, jsonify
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
    elif (request.method == 'GET'):
        # get all products
        print('fetching all products...')
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
    elif (request.method == 'PUT'):
        # update product
        print(f'updating product with id {product_id} ...')
    elif (request.method == 'DELETE'): 
        # delete product
        print(f'deleting product with id {product_id}...')
    return 'Product endpoint reached'

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
        return create
    elif (request.method == 'GET'):
        # get all categories
        print('fetching all categories...')
        categories = redis_db.get_all_categories()
        return json.dumps(categories)
    else: 
        # reject request 
        print('rejecting request')
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
        return category
    elif (request.method == 'PUT'):
        # update category
        print(f'updating category with id {category_id} ...')
    elif (request.method == 'DELETE'): 
        # delete category
        print(f'deleting category with id {category_id}...')
    return 'Product endpoint reached'