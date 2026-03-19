from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password = db.Column(db.String(255), nullable=False) # We will hash this!
    
    # Step 1: Personal Details
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    father_name = db.Column(db.String(100))
    mother_name = db.Column(db.String(100))
    birth_date = db.Column(db.Date)
    mobile = db.Column(db.String(20))
    id_number = db.Column(db.String(50))
    tax_id = db.Column(db.String(50))
    
    # Step 2: Contact Details
    email = db.Column(db.String(120), unique=True)
    country = db.Column(db.String(100), default="Kenya")
    state = db.Column(db.String(100))
    city = db.Column(db.String(100))
    zip_code = db.Column(db.String(20))
    address = db.Column(db.Text)

    # Relationship: One user can have many accounts
    accounts = db.relationship('Account', backref='owner', lazy=True)

class Account(db.Model):
    __tablename__ = 'accounts'
    
    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(20), unique=True, nullable=False)
    account_type = db.Column(db.String(20), default="Savings") # Savings, Current, etc.
    balance = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.String(100), nullable=False) # 'Deposit' or 'Withdraw'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Link this transaction to a specific account
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
