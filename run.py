from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, User, Account, Transaction
import random


app = Flask(__name__)

app.config['SECRET_KEY'] = 'dev_key_for_sky_bank_2026'

# --- CONNECTION CODE STARTS HERE ---
# Format: postgresql://username:password@localhost:5432/database_name
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Postsmf12#@localhost:5432/banking_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# This line creates the tables in Postgres automatically if they don't exist
with app.app_context():
    db.create_all()
# --- CONNECTION CODE ENDS HERE ---

@app.route('/Home')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #Grab the data from the form 
        username = request.form.get('username')
        password = request.form.get('password')
        #check if the user already exists in the database 
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))

    # GET: show login form
    return render_template('login.html', mode='login')

@app.route('/register' , methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        print('DEBUG /register POST received', request.form.to_dict())

        # Capture all data from step 1 to step 5
        #step 1 : Personal Details
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        father_name = request.form.get('father_name')
        mother_name = request.form.get('mother_name')       
        birth_date = request.form.get('birth_date')
        mobile = request.form.get('mobile')
        id_number = request.form.get('id_number')
        tax_id = request.form.get('tax_id')
        #step 2 : Contact Details   
        email = request.form.get('email')
        country = request.form.get('country')
        state = request.form.get('state')
        city = request.form.get('city')
        zip_code = request.form.get('zip_code')
        address = request.form.get('address')
        #step 3 : Account Details
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not username or not password or not confirm_password:
            flash('Username and password are required.', 'error')
            return redirect(url_for('sign_up'))

        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('sign_up'))

        # Check if the username or email already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or email already exists. Please choose another.', 'error')
            return redirect(url_for('sign_up'))
        # Create a new user instance
        new_user = User(
            username=username,
            password=password, # We will handle real hashing next
            first_name=first_name,
            last_name=last_name,
            father_name=father_name,
            mother_name=mother_name,
            birth_date=birth_date,
            mobile=mobile,
            id_number=id_number,
            tax_id=tax_id,
            email=email,
            country=country,
            state=state,
            city=city,
            zip_code=zip_code,
            address=address
        )
        # Add the new user to the database
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully! Please Login.', 'success')
            return redirect(url_for('login' , mode='login'))
        except Exception as e:
            db.session.rollback()
            return f"There was an error saving your data: {e}"
    else:
        return render_template('register.html', mode='register')

@app.route('/user')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('sign_in'))
    
    from models import User # Ensure User is imported
    user = User.query.get(session['user_id'])
    
    # 1. Create the DATA for the Charts (Lists)
    chart_labels = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    credits_list = [0, 0, 0, 0, 0]
    debits_list = [0, 0, 0, 0, 0]
    
    # 2. Create the TOTALS for the top Stat Cards (Single Numbers)
    total_credited = 0.00
    total_debited = 0.00
    recent_transactions = []

    # Get last 5 transactions for the "Transaction Graph"
    # We'll take the 5 most recent amounts to show on the bars
    chart_labels = [tx.timestamp.strftime('%a') for tx in recent_transactions[:5]][::-1]
    chart_data = [tx.amount for tx in recent_transactions[:5]][::-1]

    # Separate them into credits (positive) and debits (negative) for the bars
    credits = [amt if amt > 0 else 0 for amt in chart_data]
    debits = [abs(amt) if amt < 0 else 0 for amt in chart_data]

    return render_template('user.html', 
                           user=user, 
                           recent_transactions=recent_transactions,
                           chart_labels=chart_labels,
                           credits=credits_list,   # This goes to the Chart
                           debits=debits_list,     # This goes to the Chart
                           total_credited=total_credited, # This goes to the Card
                           total_debited=total_debited)   # This goes to the Card    

@app.route('/logout')
def logout():
    # 1. Clear the session
    session.clear() 
    
    # 2. Add a message (optional, helps for testing)
    # flash("You have been logged out.") 

    # 3. CRITICAL: Redirect the user back to the login page
    return redirect(url_for('login'))

import random

@app.route('/open-account', methods=['GET', 'POST'])
def open_account():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        selected_type = request.form.get('account_type')
        user_id = session['user_id']
        
        # --- NEW DUPLICATE CHECK ---
        # Look for an existing account for THIS user with THIS type
        existing_account = Account.query.filter_by(
            user_id=user_id, 
            account_type=selected_type
        ).first()

        if existing_account:
            flash(f'You already have a {selected_type} account!', 'error')
            return render_template('open_account.html')
        # ---------------------------

        # If no duplicate found, proceed with creation
        new_acc_no = f"SKY-{random.randint(1000000000, 9999999999)}"
        new_account = Account(
            account_number=new_acc_no,
            account_type=selected_type,
            balance=500.0,
            user_id=user_id
        )
        
        db.session.add(new_account)
        db.session.commit()
        
        flash(f'Successfully opened a {selected_type} account!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('open_account.html')

@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        amount_str = request.form.get('amount')
        account_id = request.form.get('account_id') # Which account is receiving money?
        amount = float(amount_str) if amount_str else 0.0
        
        target_account = Account.query.get(account_id)
        
        if target_account:
            # 1. Update the balance
            target_account.balance += amount
            
            # 2. Create the transaction record
            new_tx = Transaction(
                amount=amount,
                transaction_type='Deposit',
                account_id=target_account.id
            )
            
            db.session.add(new_tx)
            db.session.commit()
            
            flash(f'Successfully deposited ${amount}', 'success')
            return redirect(url_for('dashboard'))

    return render_template('deposit.html', user=user)

@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        amount_str = request.form.get('amount')
        account_id = request.form.get('account_id')
        amount = float(amount_str) if amount_str else 0.0
        
        target_account = Account.query.get(account_id)
        
        if target_account:
            # --- SECURITY CHECK ---
            if target_account.balance < amount:
                flash(f'Insufficient funds! You only have ${target_account.balance}', 'error')
                return render_template('withdraw.html', user=user)
            
            # 1. Deduct the balance
            target_account.balance -= amount
            
            # 2. Create the transaction record (recorded as negative or 'Withdraw')
            new_tx = Transaction(
                amount=-amount, # We store it as a negative number for math later
                transaction_type='Withdraw',
                account_id=target_account.id
            )
            
            db.session.add(new_tx)
            db.session.commit()
            
            flash(f'Successfully withdrew ${amount}', 'success')
            return redirect(url_for('dashboard'))

    return render_template('withdraw.html', user=user)

@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        amount = float(request.form.get('amount'))
        sender_acc_id = request.form.get('sender_account_id')
        recipient_acc_no = request.form.get('recipient_acc_no').strip()
        
        sender_acc = Account.query.get(sender_acc_id)
        # Search for the recipient by their unique Account Number (e.g., SKY-123456)
        recipient_acc = Account.query.filter_by(account_number=recipient_acc_no).first()

        # --- VALIDATIONS ---
        if not recipient_acc:
            flash('Recipient account number not found!', 'error')
        elif sender_acc.balance < amount:
            flash('Insufficient funds for this transfer!', 'error')
        elif sender_acc.account_number == recipient_acc_no:
            flash('You cannot transfer money to the same account!', 'error')
        else:
            # --- THE TRANSACTION ---
            # 1. Update Balances
            sender_acc.balance -= amount
            recipient_acc.balance += amount
            
            # 2. Create Log for Sender
            sender_tx = Transaction(
                amount=-amount,
                transaction_type=f'Transfer to {recipient_acc_no}',
                account_id=sender_acc.id
            )
            
            # 3. Create Log for Recipient
            recipient_tx = Transaction(
                amount=amount,
                transaction_type=f'Transfer from {sender_acc.account_number}',
                account_id=recipient_acc.id
            )
            
            db.session.add(sender_tx)
            db.session.add(recipient_tx)
            new_tx = Transaction(amount=amount, type='transfer', account_id=sender_acc.id)
            db.session.add(new_tx)
            db.session.commit()
            
            flash(f'Successfully transferred ${amount} to {recipient_acc_no}', 'success')
            return redirect(url_for('dashboard'))

    return render_template('transfer.html', user=user)

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/about')
def about():    
    return render_template('about.html')

@app.route('/contact')
def contact():        
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)