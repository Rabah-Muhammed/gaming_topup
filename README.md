#  Gaming Top-Up Management System

A Django-based backend system that allows users to place gaming top-up orders, and provides admins with insightful analytics via a visual dashboard. The system supports validation, RESTful APIs, and automatic documentation with Swagger/OpenAPI.

---

##  Features

-  Game & Product Models (with Django Admin)
-  Top-up API with validations
-  Swagger + ReDoc API docs via DRF Spectacular
-  Staff-only dashboard:
  -  Top 5 most purchased products
  -  Revenue for the last 7 days (with chart)
  -  Failed payment count for the current month
-  Responsive dashboard using Tailwind CSS and Chart.js

---

##  Tech Stack

- Python 3.x
- Django
- Django REST Framework
- drf-spectacular (for OpenAPI docs)
- Chart.js (for visualization)
- Tailwind CSS (for dashboard design)

---

##  Setup Instructions

```bash
# Clone the repository
git clone https://github.com/Rabah-Muhammed/gaming_topup.git
cd gaming_topup_project

# Set up a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install required packages
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create a superuser for admin access
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```
##  Top-Up API Usage
###  Endpoint
```
POST /api/topup/
```
##  Sample Request
```
{
  "gamename": "clash of clan",
  "game_id": "coc123",
  "product_name": "UC Pack 500",
  "product_id": 4,
  "product_price": 699.00,
  "user_email": "player@example.com",
  "payment_status": "pending"
}
```
##  Sample Success Response
```
{
  "message": "Top-up order created successfully."
}
```
## ! Validation Rules
   -  Game must exist and be active.
   -  Product must match the specified game, name, ID, and price.

##  Admin Dashboard
###  URL
```
/api/dashboard/
```
## Access
-  Requires staff login (admin interface authentication)

##  API Documentation
  -  OpenAPI 3.0 powered by drf-spectacular:
```
 Schema JSON → /api/schema/
 Swagger UI → /api/docs/
 ReDoc UI → /api/redoc/
```
## Contributing
  -  Fork the repository.
  -  Create a feature branch (git checkout -b feature-name).
  -  Commit changes (git commit -m "Add feature").
  -  Push to the branch (git push origin feature-name).
  -  Open a pull request.

