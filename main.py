
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

# Import your routes
from app.api.routes import auth, users
from app.middlewares.error_handler import add_exception_handlers
from app.db.session import engine, Base

# Initialize FastAPI App
app = FastAPI(title="FastAPI Backend", version="1.0.0", description="FastAPI Backend with JWT Authentication")

# Enable CORS (Modify allowed origins as per your frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routes
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])

# Register Exception Handlers
add_exception_handlers(app)

# Database Check on Startup
@app.on_event("startup")
def startup():
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database connected successfully")
    except Exception as e:
        print(f"❌ Error connecting to the database: {e}")

# Root API Check
@app.get("/")
def health_check():
    return {"message": "FastAPI backend is running!"}

# Custom OpenAPI for JWT Authentication in Swagger
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="FastAPI Backend",
        version="1.0.0",
        description="FastAPI Backend with JWT Authentication",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Apply Custom OpenAPI
app.openapi = custom_openapi
