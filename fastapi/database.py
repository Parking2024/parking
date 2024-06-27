from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlalchemy import create_engine, MetaData, Table, Column, String
from sqlalchemy.sql import select, insert, update, and_, or_
from sqlalchemy import text
from models import *
from datetime import datetime,date
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation

# Create a new engine instance
engine = create_engine('postgresql://username:password@172.26.88.105:5432/postgres')

# Initialize the metadata
metadata = MetaData()

# Reflect the tables
metadata.reflect(bind=engine)
MAX_SPOTS= 10

def add_user_db(user: User):
    # Create a new connection
    with engine.connect() as connection:

        users = Table('user_info', metadata, autoload_with=engine)
        s = select(users).where(users.c.username == user.username)
        result = connection.execute(s)
        user_exists = result.fetchone()
        if user_exists:
            raise HTTPException(status_code=400, detail="Username already exists")

        i = insert(users).values(username=user.username, password=user.password, email_id=user.email_id, name=user.name, mobile_number=user.mobile_number)
        print(str(i))
        
        try:
            result = connection.execute(i)
            connection.commit()
        except Exception as e:
            print(f"An error occurred: {e}")

    return {"message": "User created successfully"}

def get_user_db(username):
    with engine.connect() as connection:
        users = Table('user_info', metadata, autoload_with=engine)
        s = select(users).where(users.c.username == username)
        result = connection.execute(s)
        user_data = result.fetchone()
        if user_data:
            return {"message": "User found successfully"}
        else:
            raise HTTPException(status_code=404, detail="User not found")


def add_parking_db(parking: Parking):
    with engine.connect() as connection:
        parkings = Table('parking_slots', metadata, autoload_with=engine)
        p = select(parkings).where(parkings.c.parking_id == parking.parking_id)
        result = connection.execute(p)
        user_exists = result.fetchone()
        if user_exists:
            raise HTTPException(status_code=400, detail="Username already exists")
        i = insert(parkings).values(parking_id=parking.parking_id, parking_name=parking.parking_name, description = parking.description)
        print(str(i))

        try:
            result = connection.execute(i)
            connection.commit()
        except Exception as e:
            print(f"An error occurred: {e}")

    return {"message": "Parking added successfully"}

def get_available_slots():
    current_time = datetime.now()
    reservations = Table('reservation', metadata, autoload_with=engine)
    
    with engine.connect() as connection:
        query = select(reservations.c.from_datetime, reservations.c.to_datetime).where(
            and_(
                reservations.c.from_datetime <= current_time,
                reservations.c.to_datetime >= current_time
            )
        )
        result = connection.execute(query)
        active_reservations = result.rowcount
        print(active_reservations)

    available_spots = MAX_SPOTS - active_reservations
    return {"available_spots": available_spots}


def check_availability_db(username: str):
    current_date = date.today()

    with engine.connect() as connection:
        parking_slots = Table('parking_slots', metadata, autoload_with=engine)
        users = Table('user_info', metadata, autoload_with=engine)
        reservations = Table('reservation', metadata, autoload_with=engine)
        # Get all parking slots
        query = select(parking_slots.c.parking_id, parking_slots.c.parking_name, parking_slots.c.description)
        result = connection.execute(query)
        all_slots = [row[0] for row in result]

        # Get today's booking details
        query = select(reservations.c.username, reservations.c.booking_id, reservations.c.bookingdate, reservations.c.parking_id, reservations.c.from_datetime, reservations.c.to_datetime, reservations.c.comments).where(
            and_(
                reservations.c.bookingdate == current_date,
                reservations.c.username == username
            )
        )
        result = connection.execute(query)
        today_bookings = [row[0] for row in result]

        # Filter out the slots booked today
        available_slots = list(set(all_slots) - set(today_bookings))

        # Check if the user has already booked a slot
        if username in today_bookings:
            raise HTTPException(status_code=400, detail="User has already booked a slot today")

        return {"available_slots": available_slots}


def update_booking_db(booking: Reservation):
    with engine.connect() as connection:
        reservations = Table('reservation', metadata, autoload_with=engine)
        # Check if a reservation already exists for the given parking_id and username
        s = select(reservations).where(
            and_(
                reservations.c.parking_id == booking.parking_id,
                reservations.c.username == booking.username
            )
        )
        result = connection.execute(s)
        reservation_data = result.fetchone()
        print(reservation_data)
        if reservation_data is None:
            try:
                u = insert(reservations).values(
                    username=booking.username,
                    booking_id=booking.booking_id,
                    parking_id=booking.parking_id,
                    from_datetime=booking.from_datetime,
                    to_datetime=booking.to_datetime,
                    comments=booking.comments
                )
                result = connection.execute(u)
                connection.commit()
                return {"message": "Booking added successfully"}
            except IntegrityError as e:
                if isinstance(e.orig, UniqueViolation):
                    return {"message": "A reservation already exists for the given parking_id or username during the requested time "}
                else:
                    print("An error while inserting: " + str(e))
        else:
            # If a reservation already exists, return an error message
            return {"message": "A reservation already exists for the given parking_id and username during the requested time"}

def leave_spot_db(reservation: ReservationUpdate):
    with engine.connect() as connection:
        reservations = Table('reservation', metadata, autoload_with=engine)
        query = (
            update(reservations).
            where(reservations.c.booking_id == reservation.booking_id).
            values(to_datetime=reservation.to_date_time)
        )
        print(str(query))
        connection.execute(query)
        connection.commit()
    return {"message": "Reservation updated successfully"}