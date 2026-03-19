# MoneyWise | Full-Stack Online Banking System

MoneyWise is a secure, high-performance banking dashboard designed to bridge the gap between financial management and modern web technology. Built as a capstone project for my Business Computing degree at JKUAT, it demonstrates a complete integration of relational databases, secure backend logic, and interactive frontend design.

## Key Features

* **Secure Authentication**: Robust user registration and login system with encrypted password handling.
* **Financial Dashboard**: Real-time visualization of spending patterns and account balances using **Chart.js**.
* **Transaction Management**: Seamless logic for deposits and withdrawals with automatic balance updates in the database.
* **Relational Database**: Powered by **PostgreSQL** to ensure ACID compliance and data integrity for all financial records.
* **Modern UI/UX**: Designed with a **Glassmorphism** aesthetic, utilizing responsive CSS Grid and Flexbox for a premium feel.

## Technical Stack

* **Backend**: Python (Flask Framework)
* **Database**: PostgreSQL with SQLAlchemy ORM
* **Frontend**: HTML5, CSS3, JavaScript (ES6+), Chart.js
* **Deployment**: Vercel (Production Environment)

##  Project Structure


├── app/
│   ├── static/          # CSS, Images, and Chart.js logic
│   ├── templates/       # HTML layouts (Dashboard, Login, etc.)
│   ├── models.py        # SQLAlchemy Database Schema (User, Account)
│   └── routes.py        # Flask backend controllers
├── init_db.py           # Database initialization script
├── requirements.txt     # Dependencies (Flask, psycopg2, SQLAlchemy)
└── vercel.json          # Deployment configuration
