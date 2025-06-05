from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from config import Config
from services import InventoryService, StockInService, StockOutService

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'Suster' or 'doctor'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('register'))

        user = User(username=username, email=email, role=role)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()

        flash('Registration successful!')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        
        flash('Invalid username or password')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'Suster':
        products = InventoryService.get_products()
        stock_ins = StockInService.get_stock_ins()
        return render_template('dashboard.html', products=products, stock_ins=stock_ins)
    else:  # doctor
        stock_outs = StockOutService.get_stock_outs()
        return render_template('dashboard.html', stock_outs=stock_outs)

@app.route('/api/products')
@login_required
def get_products():
    products = InventoryService.get_products()
    return jsonify(products)

@app.route('/api/stock-in', methods=['POST'])
@login_required
def create_stock_in():
    if current_user.role != 'Suster':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    result = StockInService.create_stock_in(
        product_id=data['product_id'],
        quantity=data['quantity'],
        date=data['date'],
        unit_price=data.get('unit_price')
    )
    return jsonify(result)

@app.route('/api/stock-out', methods=['POST'])
@login_required
def create_stock_out():
    if current_user.role != 'doctor':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    result = StockOutService.create_stock_out(
        product_id=data['product_id'],
        quantity_used=data['quantity_used'],
        usage_date=data['usage_date'],
        issued_to_service=data.get('issued_to_service'),
        related_id=data.get('related_id')
    )
    return jsonify(result)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/inventory/products', methods=['GET'])
@login_required
def list_products():
    if current_user.role != 'Suster':
        flash('Unauthorized access')
        return redirect(url_for('dashboard'))
    
    products = InventoryService.get_products()
    categories = InventoryService.get_categories()
    suppliers = InventoryService.get_suppliers()
    return render_template('inventory/products.html', 
                         products=products, 
                         categories=categories, 
                         suppliers=suppliers)

@app.route('/inventory/products/create', methods=['GET', 'POST'])
@login_required
def create_product():
    if current_user.role != 'Suster':
        flash('Unauthorized access')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        result = InventoryService.create_product(
            name=request.form['name'],
            description=request.form['description'],
            category_id=int(request.form['category_id']),
            supplier_id=int(request.form['supplier_id']),
            quantity=int(request.form['quantity']),
            unit_price=float(request.form['unit_price']) if request.form['unit_price'] else None
        )
        
        if result and not result.get('errors'):
            flash('Product created successfully')
            return redirect(url_for('list_products'))
        else:
            flash('Error creating product')
    
    categories = InventoryService.get_categories()
    suppliers = InventoryService.get_suppliers()
    return render_template('inventory/create_product.html',
                         categories=categories,
                         suppliers=suppliers)

@app.route('/inventory/products/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    if current_user.role != 'Suster':
        flash('Unauthorized access')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        result = InventoryService.update_product(
            id=id,
            name=request.form['name'],
            description=request.form['description'],
            category_id=int(request.form['category_id']),
            supplier_id=int(request.form['supplier_id']),
            quantity=int(request.form['quantity']),
            unit_price=float(request.form['unit_price']) if request.form['unit_price'] else None
        )
        
        if result and not result.get('errors'):
            flash('Product updated successfully')
            return redirect(url_for('list_products'))
        else:
            flash('Error updating product')
    
    products = InventoryService.get_products()
    product = next((p for p in products['data']['products'] if p['id'] == id), None)
    categories = InventoryService.get_categories()
    suppliers = InventoryService.get_suppliers()
    
    return render_template('inventory/edit_product.html',
                         product=product,
                         categories=categories,
                         suppliers=suppliers)

@app.route('/inventory/products/<int:id>/delete', methods=['POST'])
@login_required
def delete_product(id):
    if current_user.role != 'Suster':
        flash('Unauthorized access')
        return redirect(url_for('dashboard'))
    
    result = InventoryService.delete_product(id)
    
    if result and not result.get('errors'):
        flash('Product deleted successfully')
    else:
        flash('Error deleting product')
    
    return redirect(url_for('list_products'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5003)  # Running on different port to avoid conflict with services 