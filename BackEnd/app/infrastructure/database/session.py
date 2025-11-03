from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.common.config import settings

# Create database engine and session maker
engine = create_engine(
    settings.DEFAULT_SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
    echo=False
)
session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    """
    Get the session and clean up after use.
    """
    db = session_maker()
    try:
        yield db
    finally:
        db.close()


