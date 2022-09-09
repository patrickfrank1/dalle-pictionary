from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from . import models, crud, populate

SQLALCHEMY_DATABASE_URL = "sqlite:///./data/sql_app.db"

engine = create_engine(
	SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create tables if they don't exist
models.Base.metadata.create_all(bind=engine)

db = SessionLocal()
# populate image table if empty
if crud.get_number_of_images(db) < 1:
	print("Table 'image' is empty, populating")
	populate.insert_images(db)
db.close()