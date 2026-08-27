import os
from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy import create_engine, text
from pydantic import BaseModel

app = FastAPI()

Instrumentator().instrument(app).expose(app)

agenda = {}
current_id = 1

class Contact(BaseMdeol):
    name: str
    phone: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the Agenda API"}

@app.post("/contacts/")
def create_contact(contact: Contact):
    global current_id
    agenda[current_id] = contact.dict()
    current_id += 1
    return {"id": current_id - 1, **contact.dict()}

@app.get("/contacts/")
def read_contacts():
    return {"count": len(agenda), "contacts": agenda}

@app.put("/contacts/{contact_id}")
def update_contact(contact_id: int, contact: Contact):
    if contact_id not in agenda:
        raise HTTPException(status_code=404, detail="Contact no found")
    agenda[contact_id] = contact.dict()
    return {"id": contact_id, **contact.dict()}

@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int):
    if contact_id not in agenda:
        raise HTTPException(status_code=404, detail="Contact not found")
    del agenda[contact_id]
    return {"status": "deleted", "id": contact_id}

@app.get("/")
def root():
    return {"message": f"Hello World!"}

@app.get("/name")
def name():
    user_name = os.getenv("USER_NAME", "World")
    return {"message": f"Hello {user_name}"}

@app.get("/test-db")
def test_db():
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "postgres")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(DATABASE_URL)
    try:
        # Open connection and execute a test query
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            db_version = result.scalar()
        return {
            "status": "success",
            "message": "Connected to database successfully!",
            "database_version": db_version,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database connection failed: {str(e)}",
        )
