# 🌿 HerbalGlow

A full-stack Flask-based herbal skincare e-commerce web application that helps users discover their skin type through an interactive quiz and purchase handmade herbal skincare products securely.

---

## 📌 Overview

HerbalGlow is a web-based herbal skincare platform developed using Flask. The application allows users to explore handmade herbal products, identify their skin type through an interactive quiz, manage a shopping cart, make secure online payments, and track their orders. The project focuses on providing a simple, user-friendly, and secure online shopping experience.

---

# ✨ Features

### 👤 User Authentication
- User Registration
- Secure Login
- Password Encryption using Werkzeug
- Session Management
- Logout Functionality

### 🌿 Skin Type Quiz
- Interactive questionnaire
- Identifies user's skin type
- Personalized skincare recommendations
- Redirects users to explore HerbalGlow products

### 🛍 Product Catalog
- Face Care Products
- Hair Care Products
- Body Care Products

### 🛒 Shopping Cart
- Add products to cart
- Increase or decrease product quantity
- Automatic total price calculation

### 💳 Secure Payment
- Razorpay Payment Gateway Integration
- Online Payment Support
- Payment Confirmation

### 📦 Order Management
- Order Success Page
- View Order History
- View Order Details

### 📞 Contact & Support
- Connect With Us page
- Customer Queries
- Feedback Submission

### 🔒 Security
- Password Hashing
- Session-Based Authentication
- Environment Variables (.env) for Secret Keys

---

# 🛠 Tech Stack

## Frontend
- HTML5
- CSS3
- Bootstrap 5
- JavaScript

## Backend
- Python
- Flask

## Database
- MySQL

## Payment Gateway
- Razorpay

## Authentication
- Werkzeug Password Hashing

---

# 📂 Project Structure

```
HerbalGlow-Ecommerce
│
├── static
│   ├── CSS
│   ├── IMAGES
│   ├── JAVASCRIPT
│   └── BOOTSTRAP
│
├── templates
│
├── app.py
├── product.py
├── db.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env
```

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/keerty318/HERBALGLOW.git
```

### 2. Navigate to the Project Folder

```bash
cd HERBALGLOW
```

### 3. Install Required Packages

```bash
pip install -r requirements.txt

```

## 4. Create a .env File

Create a `.env` file in the project root and add:

```env
FLASK_SECRET_KEY=your_secret_key
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_key_secret
```

## 5. Configure the Database

- Create a MySQL database named `herbalglow`.
- Import the `database.sql` file.
- Update the MySQL database credentials in `db.py` with your own username and password.

## 6. Run the Application

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

# 📸 Screenshots

Project screenshots will be added soon.

---

# 🔒 Security Features

- Password hashing using Werkzeug
- Secure session management
- Protected user routes
- Sensitive API keys stored using `.env`
- Environment variables ignored using `.gitignore`

---

# 🚀 Future Enhancements

- Product Search
- Wishlist
- Product Reviews & Ratings
- Email Notifications
- Order Cancellation
- Admin Dashboard
- Inventory Management
- Coupon & Discount System

---

# 👩‍💻 Developer

**Keertana Priya A**


---

# 📄 License

This project was developed for educational and learning purposes.

---
