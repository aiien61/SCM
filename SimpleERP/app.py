from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from icecream import ic

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///erp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'erp_admin'
db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)

# Order Model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)

    user = db.relationship('User', backref='orders')
    product = db.relationship('Product', backref='orders')

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user session
    return redirect(url_for('login'))

@app.route('/orders', methods=['GET', 'POST'])
def orders():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    orders_list = Order.query.all()
    products_list = Product.query.all()

    if request.method == 'POST':
        product_id = int(request.form['product_id'])
        quantity = int(request.form['quantity'])
        user_id = session['user_id']
        product = Product.query.get(product_id)

        if product and product.stock >= quantity:
            total_price = product.price * quantity
            product.stock -= quantity
            order = Order(user_id=user_id, product_id=product_id,
                          quantity=quantity, total_price=total_price)
            db.session.add(order)
            db.session.commit()
            return redirect(url_for('orders'))
        else:
            return "Insufficient stock", 400

    return render_template('orders.html', orders=orders_list, products=products_list)

@app.route('/products')
def products():
    product_list = Product.query.all()
    return render_template('products.html', products=product_list)

@app.route('/add_product', methods=['POST'])
def add_product():
    name = request.form['name']
    stock = int(request.form['stock'])
    price = float(request.form['price'])
    product = Product(name=name, stock=stock, price=price)
    db.session.add(product)
    db.session.commit()
    return redirect(url_for('products'))


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    products = Product.query.all()
    orders = Order.query.order_by(Order.id.desc()).limit(5).all()  # Get latest 5 orders
    return render_template('dashboard.html', products=products, orders=orders)

if __name__ == "__main__":
    app.run(debug=True)
