# Trip Booking API Testing Portfolio

## Overview

This project demonstrates API testing skills using:

- FastAPI
- Postman
- Newman
- GitHub Actions

## Features

- REST API with authentication
- Postman collection with automated tests
- Environment variables (Local & Codespaces)
- Newman CLI execution
- CI pipeline with GitHub Actions

## How to Run the API

cd api
uvicorn main:app --reload --host 0.0.0.0 --port 8000

## How to Run Tests Locally

newman run postman/TripBooking.postman_collection.json \
-e postman/Local.postman_environment.json \
--env-var "baseUrl=http://127.0.0.1:8000"

## CI Pipeline

Tests are automatically executed on every push using GitHub Actions.

## API Documentation

docs/API_DOCUMENTATION.md

## Tech Stack

- Python (FastAPI)
- Postman
- Newman
- GitHub Actions