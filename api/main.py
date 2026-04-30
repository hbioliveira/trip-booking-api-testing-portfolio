from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr

app = FastAPI(
    title="Trip Booking API",
    description="API for practicing API testing with Postman.",
    version="1.0.0"
)

security = HTTPBearer()

FAKE_TOKEN = "fake-jwt-token"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class BookingRequest(BaseModel):
    trip_id: int
    customer_name: str
    customer_email: EmailStr
    travelers: int


trips = [
    {
        "id": 1,
        "title": "Italy Walking Tour",
        "destination": "Italy",
        "price": 3500.00,
        "available_spots": 8,
        "activity_level": "Moderate"
    },
    {
        "id": 2,
        "title": "Portugal Bike Tour",
        "destination": "Portugal",
        "price": 2800.00,
        "available_spots": 5,
        "activity_level": "Active"
    },
    {
        "id": 3,
        "title": "Japan Cultural Adventure",
        "destination": "Japan",
        "price": 5200.00,
        "available_spots": 10,
        "activity_level": "Easygoing"
    }
]

bookings = []


def validate_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.scheme != "Bearer" or credentials.credentials != FAKE_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing authorization token"
        )


@app.get("/")
def read_root():
    return {"message": "Trip Booking API is running"}


@app.post("/auth/login")
def login(request: LoginRequest):
    if request.email == "qa@example.com" and request.password == "password123":
        return {"token": FAKE_TOKEN}

    raise HTTPException(
        status_code=401,
        detail="Invalid email or password"
    )


@app.get("/trips")
def get_trips():
    return trips


@app.get("/trips/{trip_id}")
def get_trip_by_id(trip_id: int):
    for trip in trips:
        if trip["id"] == trip_id:
            return trip

    raise HTTPException(
        status_code=404,
        detail="Trip not found"
    )


@app.post("/bookings", status_code=201, dependencies=[Depends(validate_token)])
def create_booking(request: BookingRequest):
    selected_trip = None

    for trip in trips:
        if trip["id"] == request.trip_id:
            selected_trip = trip
            break

    if selected_trip is None:
        raise HTTPException(
            status_code=404,
            detail="Trip not found"
        )

    if request.travelers <= 0:
        raise HTTPException(
            status_code=400,
            detail="Travelers must be greater than zero"
        )

    if request.travelers > selected_trip["available_spots"]:
        raise HTTPException(
            status_code=400,
            detail="Not enough available spots"
        )

    booking = {
        "id": len(bookings) + 1,
        "trip_id": request.trip_id,
        "customer_name": request.customer_name,
        "customer_email": request.customer_email,
        "travelers": request.travelers
    }

    bookings.append(booking)
    selected_trip["available_spots"] -= request.travelers

    return booking


@app.get("/bookings", dependencies=[Depends(validate_token)])
def get_bookings():
    return bookings


@app.delete("/bookings/{booking_id}", status_code=204, dependencies=[Depends(validate_token)])
def delete_booking(booking_id: int):
    for booking in bookings:
        if booking["id"] == booking_id:
            bookings.remove(booking)
            return

    raise HTTPException(
        status_code=404,
        detail="Booking not found"
    )