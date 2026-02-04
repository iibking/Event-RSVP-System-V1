from fastapi import FastAPI
from api.v1.event import event_router


app = FastAPI(title="Event RSVP System")

app.include_router(event_router, prefix="/events", tags=["Events"])


@app.get("/", status_code=200)
async def health_check():
    return {"status": "API is running"}
