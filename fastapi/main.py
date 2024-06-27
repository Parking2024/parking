
from fastapi import FastAPI
from models import User, Parking, Reservation, ReservationUpdate
import services

import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"Home": "Page"}

@app.post("/add_user")
async def add_user(user: User):
    return services.add_user(user)

@app.get("/get_user/{username}")
async def get_user(username: str):
    return services.get_user(username)

@app.post("/add_parking")
async def add_parking(parking: Parking):
    return services.add_parking(parking)

@app.get("/get_parking_details")
async def get_parking_details():
    return services.get_parking_details()

@app.get("/check_availability/{username}")
async def check_availability(username: str):
    return services.check_availability(username)

@app.post("/update_booking")
async def update_booking(reservation: Reservation):
    return services.update_booking(reservation)

@app.post("/leave_spot")
async def leave_spot(reservationUpdate: ReservationUpdate):
    return services.leave_spot_db(reservationUpdate)

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
