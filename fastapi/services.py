from models import User, Parking, Reservation
from database import *
import datetime

users = []
parkings = []
reservations = []

def add_user(user: User):
    add_user_db(user)
    return {"message": "User added successfully"}

def get_user(username: str):
    user = get_user_db(username)
    return user

def add_parking(parking: Parking):
    add_parking_db(parking)
    return {"message": "Parking added successfully"}

def get_parking_details():
    parkings = get_available_slots()
    return parkings

def check_availability(username: str):
    return check_availability_db(username)

def update_booking(bookingUpdate: Reservation):
    return update_booking_db(bookingUpdate)

def leave_spot(reservationUpdate: ReservationUpdate):
    return leave_spot_db(reservationUpdate)
