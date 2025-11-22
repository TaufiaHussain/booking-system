# Django Appointment Booking Starter Kit

A complete, production-ready Django appointment booking system with:

- Modern Tailwind UI  
- Appointment booking form  
- Automatic emails to customer & admin  
- PDF confirmation attachment  
- Admin dashboard with charts & stats  
- Working-hours logic  
- No past bookings / no double booking  
- EN/DE language toggle  
- Simple deployment (Render, Railway, DigitalOcean)  

---

##  Features

### ✔ Booking Form
- Name, Email, Phone, Date, Time  
- Prevents:
  - Past dates  
  - Sundays  
  - Double booking  
  - Outside working hours (09:00–18:00)

### ✔ Admin Panel
- Manage bookings  
- Confirm bookings with one click  
- Automatic confirmation email with PDF  
- Status filtering  
- Default Django admin included  

### ✔ Dashboard
- Today's appointments  
- Pending confirmations  
- Last 7 days chart (Chart.js)  
- Clean Tailwind UI  

### ✔ Email System
- Emails customer when booking is created  
- Emails admin when booking arrives  
- Sends PDF confirmation when booking is confirmed  
- All templates stored in the database (editable without code)

### ✔ Language Toggle
- EN ↔ DE switch  
- Works via session  
- UI text updates dynamically  

---

##  Requirements

- Python 3.10+  
- Django 5+  
- SQLite (default)  
- virtualenv recommended  

---

## 🛠 Installation

### 1. Create a folder & virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run migrations
```bash
python manage.py migrate
```

### 4. Create superuser
```bash
python manage.py createsuperuser
```

### 5. Start the development server
```bash
python manage.py runserver
```

Visit:
- Public booking page → http://127.0.0.1:8000  
- Admin dashboard → http://127.0.0.1:8000/admin-dashboard  
- Django admin → http://127.0.0.1:8000/admin  

---

##  Folder Structure

```
booking_app/
│
├── config/
├── bookings/
│   ├── templates/bookings/
│   ├── utils.py
│   ├── forms.py
│   ├── models.py
│   └── views.py
│
├── static/
├── manage.py
├── requirements.txt
└── README.md
```

---

##  Email Testing (Console)
During development, all emails appear in the terminal automatically using Django’s console backend.

No external email service needed.

---

##  Deployment

You can deploy this app to:

### Render.com
- Free tier available  
- Automatic deploy from GitHub  

### Railway.app  
### DigitalOcean App Platform  
### Heroku (if you want automated PDF generation)

---

##  License
This project is provided with a **commercial license**.  
You may use it in client projects or your own SaaS.

Redistribution of the source code as a competing product is allowed only with substantial modification.

---

##  Support
For questions, improvements, or custom versions, contact the developer.
info@datalens.tools
