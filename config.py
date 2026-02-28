import os 
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-key'
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}@postgresql/{os.environ.get('POSTGRES_DB')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    QR_URL = os.environ.get('QR_URL') or 'http://localhost:5000/tech/view_tech/'