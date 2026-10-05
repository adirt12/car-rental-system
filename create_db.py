from app.db import Base, engine
from app.models import Car, Rental

Base.metadata.create_all(bind=engine)

print("Database created")