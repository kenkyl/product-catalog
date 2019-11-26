from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Wilkommen, Leute!'


@app.route('/products')
def get_all_products():
    return ''

@app.route('/products/<int:product_id')
def get_product_by_id(product_id):
    return ''