from fastapi import APIRouter, status, Form, UploadFile, File, HTTPException
from typing import Optional, List
from schemas.event_schema import Event, RSVP
from core.db import events, rsvps


event_router = APIRouter()


# POST /events/ - Create a new event
@event_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_event(
    title: str = Form(...),
    description: str = Form(...),
    date: str = Form(...),
    location: str = Form(...),
    flyer: Optional[UploadFile] = File(None)
):
    event_id = len(events) + 1
    flyer_filename = flyer.filename if flyer else None
    
    new_event = {
        "id": event_id,
        "title": title,
        "description": description,
        "date": date,
        "location": location,
        "flyer_filename": flyer_filename,
        "rsvps": []
    }
    events.append(new_event)
    return new_event


# GET /events/ - List all events
@event_router.get("/", response_model=List[Event])
def get_all_events():
    return events


# GET /events/{event_id} - Get event by id
@event_router.get("/{event_id}", response_model=Event)
def get_event_by_id(event_id: int):
    for event in events:
        if event["id"] == event_id:
            return event
    raise HTTPException(status_code=404, detail="Event not found")


# POST /events/{event_id}/rsvp - RSVP to an event
@event_router.post("/{event_id}/rsvp", status_code=status.HTTP_201_CREATED)
async def create_rsvp(
    event_id: int,
    name: str = Form(...),
    email: str = Form(...)
):
    # Find the event
    for event in events:
        if event["id"] == event_id:

            # Check if user has already RSVPed
            for rsvp in rsvps:
                if rsvp["event_id"] == event_id and rsvp["email"] == email:
                    raise HTTPException(status_code=400, detail="Already RSVPed")
                
            # Create RSVP
            rsvp_data = {"name": name, "email": email, "event_id": event_id}
            rsvps.append(rsvp_data)
            # Add email to event's rsvps list
            event["rsvps"].append(email)
            return {"message": "RSVP created successfully", "rsvp": rsvp_data}
    
    raise HTTPException(status_code=404, detail="Event not found")


# GET /events/{event_id}/rsvps - Get list of RSVPs for an event
@event_router.get("/{event_id}/rsvps")
def get_event_rsvps(event_id: int):
    # Check if event exists
    event_exists = False
    for event in events:
        if event["id"] == event_id:
            event_exists = True
            break
    
    if not event_exists:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Get all RSVPs for this event
    event_rsvps = [rsvp for rsvp in rsvps if rsvp["event_id"] == event_id]
    return event_rsvps