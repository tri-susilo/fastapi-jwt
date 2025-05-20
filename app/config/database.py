from sqlalchemy import create_engine                                              # digunakan untuk membuat koneksi ke database
from sqlalchemy.orm import sessionmaker, declarative_base                         # digunakan untuk membuat session dan mendeklarasikan model
from dotenv import load_dotenv                                                    # digunakan untuk memuat variabel lingkungan dari file .env
import os                                                                         # digunakan untuk mengakses variabel lingkungan                                      


# Load environment variables from .env file
load_dotenv(override=True)


# Database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()