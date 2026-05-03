from fastapi import FastAPI
from database import Base, engine
from api import usuarios, laboratorios, servicios, tickets

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mesa de Servicios - Laboratorios",
    description="API para gestión de tickets de servicios en laboratorios universitarios",
    version="1.0.0"
)

# Registrar routers
app.include_router(usuarios.router)
app.include_router(laboratorios.router)
app.include_router(servicios.router)
app.include_router(tickets.router)


@app.get("/")
def root():
    return {"message": "Mesa de Servicios API"}
