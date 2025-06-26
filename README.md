# 🎮 Gaming Top-Up Management System

A Django-based backend system that allows users to place gaming top-up orders, handle transactions reliably, and provides admins with advanced business analytics through a visual dashboard. The system supports JWT authentication, payment transaction syncing, exportable reports, and API documentation.

---

## ✅ Features

- **Authentication & User Management**
  - JWT-based login & refresh
  - User registration with profile info

- **Top-Up System**
  - Validated game & product selection
  - Auto-created payment transaction with UUID
  - Payment status webhook support
  - Signal to sync TopUpOrder status with transaction

- **Admin Dashboard (Staff Only)**
  - 📈 Daily Top-Up Revenue (last 30 days)
  - 🔥 Top 5 Most Purchased Products
  - 🎮 Game-wise Revenue Distribution
  - 👤 Most Active Users (by number of orders)
  - 📆 Date Range Filtering
  - ❌ Monthly Failed Payment Count

- **CSV Export**
  - 🧾 All Top-Up Orders → `/api/export/orders/`
  - 🚫 Failed Transactions → `/api/export/failures/`

- **API Docs**
  - Swagger UI → `/api/docs/`
  - ReDoc UI → `/api/redoc/`
  - OpenAPI Schema JSON → `/api/schema/`

- **Frontend Dashboard**
  - Built with TailwindCSS & Chart.js
  - Clean UI with real-time analytics
  - Filter and export buttons

---

## 🛠 Tech Stack

- Python 3.x
- Django
- Django REST Framework
- drf-spectacular
- Simple JWT (Auth)
- TailwindCSS (UI)
- Chart.js (Charts)

---

## ⚙️ Setup Instructions

```bash
# Clone the repository
git clone https://github.com/Rabah-Muhammed/gaming_topup.git
cd gaming_topup_project

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

---

## 🔐 Authentication

| Endpoint             | Method | Description             |
|----------------------|--------|--------------------------|
| `/api/register/`     | POST   | Register a new user      |
| `/api/token/`        | POST   | Obtain access token      |
| `/api/token/refresh/`| POST   | Refresh JWT token        |

---

## 💳 Top-Up API

**Endpoint:**
```
POST /api/topup/
```

**Sample Request:**
```json
{
  "gamename": "clash of clan",
  "game_id": "coc123",
  "product_name": "UC Pack 500",
  "product_id": 4,
  "product_price": 699.00
}
```

**Success Response:**
```json
{
  "message": "Top-up order created successfully.",
  "transaction_id": "xxxx-xxxx-uuid",
  "status": "pending"
}
```

**Validation Rules:**
- Game must exist and be active.
- Product must match name, ID, price, and game.

---

## 🔁 Payment Webhook

**Endpoint:**
```
POST /api/payment/webhook/
```

**Payload Example:**
```json
{
  "transaction_id": "xxxx-uuid",
  "status": "success"
}
```

This updates both `PaymentTransaction` and related `TopUpOrder` status automatically.

---

## 📊 Admin Dashboard

**URL:** `/api/dashboard/`  
**Access:** Staff-only

**Features:**
- Daily revenue chart & table
- Most purchased products
- Game-wise revenue bar chart
- Most active users table
- Date filtering
- CSV export

**Filter Example:**
```
/api/dashboard/?start_date=2025-06-01&end_date=2025-06-25
```

---

## 📁 CSV Export Endpoints

| Endpoint                  | Description                 |
|---------------------------|-----------------------------|
| `/api/export/orders/`     | Export all orders           |
| `/api/export/failures/`   | Export failed transactions  |

Each returns a downloadable `.csv` file.

---

## 📘 API Documentation

| Tool      | URL              |
|-----------|------------------|
| Swagger   | `/api/docs/`     |
| ReDoc     | `/api/redoc/`    |
| Schema    | `/api/schema/`   |

---

## 🤝 Contributing

```bash
# Fork the repo
# Create a feature branch
git checkout -b feature-name

# Make changes, commit, and push
git commit -m "Add feature"
git push origin feature-name
```

Then open a pull request 🚀

---

## 🧠 Business Insights Powered By

- Chart.js for interactive analytics
- Django ORM for optimized aggregations
- TailwindCSS for responsive UI
- Secure backend powered by Django & DRF

---

## 📸 Preview

Access the dashboard at:

```
http://localhost:8000/api/dashboard/
```

Use staff login credentials to view analytics & export options.

---

