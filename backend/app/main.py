from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import (
    overview,
    delivery,
    inventory,
    revenue,
    order_quality,
    store_performance,
    alerts,
    insights,
    data_management,
    reports,
    metadata
)

app = FastAPI(
    title="QuickCommerce Intelligence API",
    description="Enterprise Business Intelligence Platform for Quick Commerce Operations (Blinkit / Zepto / Swiggy Instamart)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(overview.router, prefix="/api")
app.include_router(delivery.router, prefix="/api")
app.include_router(inventory.router, prefix="/api")
app.include_router(revenue.router, prefix="/api")
app.include_router(order_quality.router, prefix="/api")
app.include_router(store_performance.router, prefix="/api")
app.include_router(alerts.router, prefix="/api")
app.include_router(insights.router, prefix="/api")
app.include_router(data_management.router, prefix="/api")
app.include_router(reports.router, prefix="/api")
app.include_router(metadata.router, prefix="/api")

@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": "QuickCommerce Intelligence API",
        "version": "1.0.0"
    }

@app.get("/", tags=["Root"])
def root():
    return {
        "message": "QuickCommerce Intelligence Operations Analytics Platform",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
