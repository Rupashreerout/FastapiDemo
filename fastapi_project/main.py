from fastapi import FastAPI
from router import user, customer,login
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    login.router,
    prefix="/Login",
    tags=['Login']
)

# Include routers
app.include_router(
    user.router,
    prefix="/user",
    tags=["user"]
)

app.include_router(
    customer.router,
    prefix="/Customer",
    tags=["customer"]
)



