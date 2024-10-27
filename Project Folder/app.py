from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Needed for session management
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Session timeout
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Initialize database
with app.app_context():
    db.create_all()

# Home route - Displays login page
@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

# Route for displaying the registration page
@app.route('/register-page', methods=['GET'])
def register_page():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('register.html')

# Login route - Handles login form submissions with POST method
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login form data
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Authenticate user
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            # Set up the session for the logged-in user
            session['user_id'] = user.id
            session.permanent = True  # Make session permanent to apply timeout
            return redirect(url_for('dashboard'))

        flash("Invalid email or password", "error")
        return redirect(url_for('home'))
    
    # Render login page if method is GET
    return render_template('login.html')

# Dashboard route - Restricted to logged-in users
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    return render_template('dashboard.html')  # Render dashboard template

# Register route - Handles registration form submissions with POST method
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle registration form data
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if email already exists
        if User.query.filter_by(email=email).first():
            flash("Email already registered", "error")
            return redirect(url_for('register_page'))

        # Hash password and save new user
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # Flash success message for registration and redirect to login page
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('home'))
    
    # Render register page if method is GET
    return render_template('register.html')

# Logout route - Ends the session
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
