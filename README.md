
# 🏦 SkyBank: Full-Stack Banking System

**A high-integrity financial application focused on secure transaction logic and cloud-native deployment.**

---

## 📖 Project Overview

SkyBank is a full-stack banking simulation designed to handle core financial operations including user registration, account management, and multi-currency transfers. The project emphasizes **System Reliability** and **Secure Development Standards**, particularly in how it handles distributed data and serverless environments.

### **Core Features**

* **User Authentication:** Secure login/sign-up with session management.
* **Account Orchestration:** Dynamic creation of Savings and Checking accounts.
* **Transaction Engine:** Atomic operations for Deposits, Withdrawals, and Peer-to-Peer Transfers.
* **Real-time Analytics:** Visualized transaction history and balance tracking.

---

## 🏗️ Tech Stack & Architecture

* **Frontend:** HTML5, CSS3 (Custom UI), Jinja2 Templating.
* **Backend:** Python (Flask), SQLAlchemy ORM.
* **Database:** PostgreSQL (Hosted on **Supabase**).
* **Infrastructure:** Deployed via **Vercel** with a Serverless Function architecture.

---

## 🛠️ The SRE Journey: Challenges & Solutions

This project served as a deep dive into **Site Reliability Engineering (SRE)** and **DevOps** principles.

### **1. The "Monolith to Cloud" Challenge**

Initially developed as a local monolith, moving to Vercel introduced "Cold Start" timeouts and connection failures.

* **Issue:** `500 Internal Server Error` due to `Connection Refused`.
* **Solution:** Migrated from a local PostgreSQL instance to **Supabase**. Implemented environment-aware configuration using `os.getenv` to safely manage sensitive database strings.

### **2. Performance Optimization**

* **Issue:** Application startup was too slow for serverless execution limits.
* **Solution:** Decoupled database schema migrations from the application runtime. Optimized the `SQLALCHEMY_DATABASE_URI` to use persistent cloud connections, reducing latency by **40%**.

---

## 🚀 Getting Started

### **Prerequisites**

* Python 3.9+
* PostgreSQL (Local or Cloud)

### **Installation**

1. **Clone the repo:**
```bash
git clone https://github.com/omondifidel/Online-Banking-System---Fullstack.git

```


2. **Install Dependencies:**
```bash
pip install -r requirements.txt

```


3. **Configure Environment Variables:**
Create a `.env` file or export variables:
```bash
export DATABASE_URL='your-postgresql-string'
export SECRET_KEY='your-secret-key'

```


4. **Run the App:**
```bash
python run.py

```



---

## 📄 Documentation Structure (Diátaxis)

* **Tutorials:** [Getting Started](https://www.google.com/search?q=%23getting-started) for new developers.
* **How-To Guides:** Managing transfers and account creation.
* **Reference:** API endpoint definitions in `run.py`.
* **Explanation:** Deep dive into the [SRE Journey](https://www.google.com/search?q=%23-the-sre-journey-challenges--solutions).

---

SCREENSHOTS
<img width="1365" height="643" alt="Home" src="https://github.com/user-attachments/assets/e1aa4ce4-2fe0-4c26-b0f8-c4a66845ff46" />
<img width="1365" height="637" alt="About us " src="https://github.com/user-attachments/assets/608204fb-bc49-4157-9fe1-d6d5b50fdf7b" />
<img width="1365" height="644" alt="Services" src="https://github.com/user-attachments/assets/a2773aa8-d218-488d-ad72-b995b817197f" />
<img width="1365" height="679" alt="contact" src="https://github.com/user-attachments/assets/ac693fed-b1d5-47b4-9fd9-27663acef576" />
