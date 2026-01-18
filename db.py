from sqlalchemy import create_engine

db_url = "sqlite:///db.db"
engine = create_engine(db_url)