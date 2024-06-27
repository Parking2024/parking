from pydantic import BaseModel
from typing import Optional
import datetime

class User(BaseModel):
    username: str
    password: str
    email_id: str
    name: str
    mobile_number: str

class Parking(BaseModel):
    parking_id: str
    parking_name: str
    description: str

class Reservation(BaseModel):
    username: str
    booking_id: str
    bookingdate: datetime.date
    parking_id: str
    from_datetime: datetime.datetime
    to_datetime: datetime.datetime
    comments: Optional[str] = None

class ReservationUpdate(BaseModel):
    booking_id: str
    to_date_time: datetime.datetime