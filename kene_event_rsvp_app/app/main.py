from fastapi import FastAPI
from kene_event_rsvp_app.app.api.events import router



app = FastAPI()

app.include_router(router)