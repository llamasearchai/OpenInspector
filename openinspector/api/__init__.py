from fastapi import FastAPI, Depends
from .routes import router
from ..database import init_db, get_session, AsyncSession

app = FastAPI(title="OpenInspector API", version="0.1.0")
app.include_router(router)

# Entry point

@app.on_event("startup")
async def _startup() -> None:  # pragma: no cover
    await init_db()

def run():  # pragma: no cover
    import uvicorn
    from ..config import settings

    uvicorn.run("openinspector.api:app", host=settings.api_host, port=settings.api_port, reload=False) 