from fastapi import FastAPI, File, UploadFile, HTTPException, status, Form,APIRouter
from typing import Optional,Annotated
import shutil


from kene_event_rsvp_app.app.schemas.event import CreateEvent,EventResponse
from kene_event_rsvp_app.app.schemas.rsvp import RsvpCreate,RsvpResponse
from kene_event_rsvp_app.app.storage.storage import events,rsvp


router = APIRouter(prefix="/event", tags=["Events"])




  





@router.post("",response_model= EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(
    title: str = Form(...),
    description: str = Form(...),
    date: str = Form(...),
    location: str = Form(...),
    flyer: Optional[UploadFile] = File(None)
):

    event_id = len(events) + 1
    flyer_data = None
    
    if flyer:
        flyer_data = flyer.filename
        with open(flyer_data, "wb") as event_object:
            shutil.copyfileobj(flyer.file, event_object)

    event = {
        "id": event_id,
        "title": title,
        "description": description,
        "date": date,
        "location": location,
        "flyer": flyer_data,
    }

    events[event_id] = event
    return event


@router.get("/")
def list_all_events():
    return list(events.values())



@router.post("/{event_id}", status_code=status.HTTP_201_CREATED)
def create_rsvp(event_id: int, rsvp_data: RsvpCreate):
    if event_id not in events:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event Id not found")
    new_rsvp = {
        "name": rsvp_data.name,
        "email": rsvp_data.email
    }
    
    rsvp[event_id].append(new_rsvp)
    return {"message": "rsvp added successfully",
            "id": event_id,
            "total_rsvps": len(rsvp[event_id]),
            "rsvp": rsvp[event_id],
            }


@router.get("/{event_id}", status_code=status.HTTP_200_OK)
def get_rsvp(event_id: int):
    if event_id not in rsvp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event id not found")
    return {
        "event_id": event_id,
        "rsvps": rsvp[event_id]
    }