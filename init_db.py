from run import app
from models import db, User, Account

def initialize():
    with app.app_context():
        print("--- Connecting to PostgreSQL ---")
        # This command tells SQLAlchemy to create all tables defined in models.py
        db.create_all()
        print("--- Tables Created Successfully! ---")
        
        # Let's add a test user so we have something to see in the dashboard
        test_user = User.query.filter_by(username='patilmohan').first()
        if not test_user:
            new_user = User(
                username='patilmohan',
                first_name='Patil',
                last_name='Mohan',
                email='test@skybank.com',
                password='hashed_password_here' # We'll handle real hashing next
            )
            db.session.add(new_user)
            db.session.commit()
            
            # Give the user an initial account and balance
            new_account = Account(
                account_number='SB-100200300',
                balance=1500.50,
                owner=new_user
            )
            db.session.add(new_account)
            db.session.commit()
            print("--- Test User 'patilmohan' Created with $1500.50 balance ---")

if __name__ == "__main__":
    initialize()