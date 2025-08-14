# 🛒 Groceries Backend Service

A **Django REST Framework**-based backend for managing products, categories, customers, and orders.  

**Features include:**
- 🔐 **OpenID Connect (OIDC) Authentication** via `mozilla-django-oidc`
- 🗂 **Hierarchical product categories** with `django-mptt`
- 📩 **Africa's Talking SMS** notifications for customers
- 📧 **Email alerts** for administrators
- 📜 **Interactive API documentation** with `drf-yasg`
- 🧪 **Automated testing** with `pytest`

---

## ⚡ Quick Start
```bash
# 1️⃣ Clone repository
git clone https://github.com/yourusername/groceries-backend.git
cd groceries-backend

# 2️⃣ Copy env file and edit credentials
cp exampleEnv .env

# 3️⃣ Install & run
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
````

---

## 📖 Table of Contents

1. [Overview](#-overview)
2. [Tech Stack](#-tech-stack)
3. [Setup](#-setup)
4. [Environment Variables](#-environment-variables)
5. [Running Locally](#-running-locally)
6. [Running Tests](#-running-tests)
7. [API Documentation](#-api-documentation)
8. [Folder Structure](#-folder-structure)
9. [License](#-license)

---

## 🔍 Overview

This backend service is designed for a grocery business. It allows:

* Managing **products** with nested **categories**
* Sending **SMS notifications** when events occur (e.g., new order placed)
* Authenticating users securely via **OIDC**
* Providing a fully interactive API for developers

---

## 🛠 Tech Stack

* **Backend**: Django, Django REST Framework
* **Authentication**: mozilla-django-oidc
* **Database**: PostgreSQL
* **Messaging**: Africa's Talking SMS API
* **Documentation**: drf-yasg (Swagger/ReDoc)
* **Testing**: pytest

---

## ⚙ Setup

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/groceries-backend.git
cd groceries
```

### 2. Set Environment Variables

Copy `exampleEnv` to `.env` and update with your credentials:

```bash
cp exampleEnv .env
```

You **must** set:

* **Database credentials** (`DATABASE_URL`)
* **OIDC credentials** (`OIDC_CLIENT_ID`, `OIDC_CLIENT_SECRET`, etc.)
* **Africa's Talking API keys**
* **Email SMTP settings**

### 3. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Start Development Server

```bash
python manage.py runserver
```

---

## 🔑 Environment Variables

Set the environment variable as shown in the exampleEnv file


## 💻 Running Locally

1. Make sure PostgreSQL is running and accessible
2. Ensure `.env` is configured
3. Run the server:

```bash
python manage.py runserver
```

4. Access the API at:

   * Swagger UI → [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
   * ReDoc → [http://localhost:8000/redoc/](http://localhost:8000/redoc/)
   * Auth → [http://localhost:8000/oidc/authenticate/](http://localhost:8000/oidc/authenticate/)

---

## 🧪 Running Tests

Before testing, ensure `.env` is set (tests may depend on some env values).

Run tests:

```bash
pytest
```

Verbose mode:

```bash
pytest -v
```

---

## 📂 Folder Structure

```
groceries/
├── categories/       # Category model & API
├── customers/        # Customer model & API
├── orders/           # Order management
├── products/         # Product management
├── config/           # Project settings
├── exampleEnv        # Example environment variables file
├── manage.py         # Django CLI
├── requirements.txt  # Python dependencies
└── README.md
```

---

## 📜 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

```