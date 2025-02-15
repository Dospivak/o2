import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    MEMBERS_FILE = os.getenv('MEMBERS_FILE', 'members.json') 