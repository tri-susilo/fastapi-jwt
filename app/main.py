from fastapi import FastAPI
from app.routes import auth_route, user_route, product_route
from app.config.database import Base, engine
from app.models import user
from app.routes import product_route


Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(auth_route.router)
app.include_router(user_route.router)
app.include_router(product_route.router)
app.include_router(product_route.router)

