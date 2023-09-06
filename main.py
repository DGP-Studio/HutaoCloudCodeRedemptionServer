from fastapi import FastAPI
import uvicorn
from routers import management, user

app = FastAPI(redoc_url=None, root_path="/code")
app.include_router(management.router)
app.include_router(user.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
