# Inventory Management System Frontend

This is the frontend application for the Inventory Management System, built with Flask and Jinja2 templates.

## Features

- User authentication (Login/Register)
- Role-based access control (Sister/Doctor)
- Responsive dashboard for different roles
- Bootstrap 5 UI components
- Flash messages for user feedback

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
.\venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Make sure you're in the frontend directory:
```bash
cd frond-end
```

2. Run the Flask application:
```bash
python app.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

## Project Structure

```
frond-end/
├── static/
│   └── css/
│       └── style.css
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
├── app.py
├── requirements.txt
└── README.md
```

## User Roles

1. Sister Role:
- Manage inventory stock levels
- Record new stock arrivals
- View inventory reports

2. Doctor Role:
- Request items from inventory
- View request history

## Development

To modify the application:

1. Templates are in the `templates/` directory
2. Static files (CSS, JS) are in the `static/` directory
3. Main application logic is in `app.py`

## Security Notes

- Change the `SECRET_KEY` in `app.py` before deploying
- Use environment variables for sensitive data
- Enable HTTPS in production 