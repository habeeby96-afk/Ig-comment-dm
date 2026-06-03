import os
from fastapi import FastAPI
from routes.webhook import router as webhook_router
from routes.dashboard import router as dashboard_router

app = FastAPI()
app.include_router(webhook_router)
app.include_router(dashboard_router)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
