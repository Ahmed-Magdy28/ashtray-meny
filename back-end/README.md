# **E-Commerce Platform**

## **Project Overview**
This project is a robust, scalable **e-commerce platform** developed using **Django** and **Django REST Framework (DRF)**. It allows users to register, log in, manage their profiles, browse products, create orders, write reviews, and shop owners to manage their shops and inventory.

The platform supports **JWT-based authentication**, features a fully-functional **CRUD API** for managing products, categories, and orders, and offers **role-based access control** for users and shop owners.

---

## **Features**

- **User Authentication**:
  - Register, login, and manage user profiles with **JWT authentication**.
  - Role-based access for **admins**, **shop owners**, and **customers**.
  
- **Product and Shop Management**:
  - CRUD operations for products, shops, and categories.
  - Product listing, search, filtering, and pagination.
  
- **Order Management**:
  - Create, update, and track orders with real-time status.
  - Integration with **wishlist** and shopping cart functionality.

- **Review and Rating System**:
  - Customers can leave reviews and rate products.
  - Shop reviews and ratings aggregation.

- **Swagger API Documentation**:
  - Easy-to-use **API documentation** using Swagger (drf_spectacular).

---

## **Technologies Used**

- **Backend**:
  - [Django](https://www.djangoproject.com/) - Python web framework.
  - [Django REST Framework](https://www.django-rest-framework.org/) - For building RESTful APIs.
  - [PostgreSQL](https://www.postgresql.org/) - Relational database system.
  
- **Authentication**:
  - [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) - Token-based authentication.

- **API Documentation**:
  - [drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/) - API schema and documentation generator.

- **Testing**:
  - [Django Test Framework](https://docs.djangoproject.com/en/stable/topics/testing/) - Automated testing.

---

## **Getting Started**

### **Prerequisites**
Make sure you have the following installed on your system:

- **Python** (>= 3.7)
- **PostgreSQL**
- **pipenv** (optional, for managing virtual environments)

### **Setup Instructions**

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/ecommerce-platform.git
   cd ecommerce-platform

2. **Create a virtual environment and install dependencies**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt

3. **Set up PostgreSQL Database**:
   - Create a PostgreSQL database:
   ```sql
   Set up PostgreSQL Database
   ```
   - Update the .env file with your database credentials:
   ```plaintext
   DB_NAME=ecommerce_db
   DB_USER=your_db_user
   DB_PASS=your_db_password
   DB_HOST=localhost
   DB_PORT=5432

5. **Run database migrations**:
   ```bash
   python manage.py migrate

6. **Create a superuser (admin)**:
   ```bash
   python manage.py createsuperuser

7. **Access the application**:
   - Admin panel: http://localhost:8000/admin/
   - API documentation (Swagger): http://localhost:8000/api/docs/
