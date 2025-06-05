class Config:
    # Service URLs
    INVENTORY_SERVICE_URL = "http://localhost:5000"
    STOCK_IN_SERVICE_URL = "http://localhost:5001"
    STOCK_OUT_SERVICE_URL = "http://localhost:5002"

    # Flask Config
    SECRET_KEY = 'your-secret-key'  # Change this in production
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False 