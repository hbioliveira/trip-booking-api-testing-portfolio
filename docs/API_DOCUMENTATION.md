# Trip Booking API Documentation

## Overview

The Trip Booking API is a practice project created to support API testing activities using FastAPI, Swagger, Postman, and later Newman.

The API allows users to list trips, authenticate with a fake token, create bookings, list bookings, and delete bookings.

## Base URL

Local development:

http://127.0.0.1:8000

GitHub Codespaces example:

https://your-codespace-url-8000.app.github.dev

---

## Authentication

Some endpoints require Bearer Token authentication.

### Login credentials

{
  "email": "qa@example.com",
  "password": "password123"
}

### Token returned

{
  "token": "fake-jwt-token"
}

### Authorization header

Authorization: Bearer fake-jwt-token

---

## Endpoints

## GET /

### Description

Checks if the API is running.

### Expected Status Code

200 OK

### Response Example

{
  "message": "Trip Booking API is running"
}

---

## POST /auth/login

### Description

Authenticates a user and returns a fake Bearer token.

### Request Body

{
  "email": "qa@example.com",
  "password": "password123"
}

### Expected Status Code

200 OK

### Response Example

{
  "token": "fake-jwt-token"
}

### Negative Scenario

Invalid credentials should return:

401 Unauthorized

{
  "detail": "Invalid email or password"
}

---

## GET /trips

### Description

Returns all available trips.

### Expected Status Code

200 OK

### Response Example

[
  {
    "id": 1,
    "title": "Italy Walking Tour",
    "destination": "Italy",
    "price": 3500.0,
    "available_spots": 8,
    "activity_level": "Moderate"
  }
]

---

## GET /trips/{trip_id}

### Description

Returns a specific trip by ID.

### Path Parameter

- trip_id (integer, required): Trip identifier

### Expected Status Code

200 OK

### Negative Scenario

If the trip does not exist:

404 Not Found

{
  "detail": "Trip not found"
}

---

## POST /bookings

### Description

Creates a booking for a selected trip.

### Authentication

Required.

### Request Body

{
  "trip_id": 1,
  "customer_name": "Gabriela Oliveira",
  "customer_email": "gabriela@example.com",
  "travelers": 2
}

### Expected Status Code

201 Created

### Response Example

{
  "id": 1,
  "trip_id": 1,
  "customer_name": "Gabriela Oliveira",
  "customer_email": "gabriela@example.com",
  "travelers": 2
}

### Negative Scenarios

Missing or invalid token:

403 Forbidden

Trip does not exist:

404 Not Found

{
  "detail": "Trip not found"
}

Travelers value is zero or negative:

400 Bad Request

{
  "detail": "Travelers must be greater than zero"
}

Not enough available spots:

400 Bad Request

{
  "detail": "Not enough available spots"
}

---

## GET /bookings

### Description

Returns all created bookings.

### Authentication

Required.

### Expected Status Code

200 OK

### Response Example

[
  {
    "id": 1,
    "trip_id": 1,
    "customer_name": "Gabriela Oliveira",
    "customer_email": "gabriela@example.com",
    "travelers": 2
  }
]

---

## DELETE /bookings/{booking_id}

### Description

Deletes a booking by ID.

### Authentication

Required.

### Path Parameter

- booking_id (integer, required): Booking identifier

### Expected Status Code

204 No Content

### Negative Scenario

If the booking does not exist:

404 Not Found

{
  "detail": "Booking not found"
}