# Auth Service

Auth Service is a microservice responsible for user authentication and authorization in the Microshop project.

## Features

- **User registration** (`sign-up`) with phone and password.
- **User login** (`sign-in`) returning **access** and **refresh** tokens.
- **JWT-based access tokens** for authenticated requests.
- **Refresh tokens** for issuing new access tokens.
- **Logout** functionality to revoke refresh tokens.
- **User profile retrieval** (`/me`) for authenticated users.
- **Secure password hashing** using bcrypt.
- **Optional multi-device support** for refresh tokens.
- **Async database access** via SQLAlchemy.

## API Endpoints

- `POST /api/v1/sign-up` - Register a new user.
- `POST /api/v1/sign-in` - Login and get access + refresh tokens.
- `POST /api/v1/refresh` - Exchange a refresh token for a new token pair.
- `POST /api/v1/logout` - Revoke a refresh token (logout).
- `GET /api/v1/me` - Get profile of the current authenticated user.
- Future endpoints for confirming phone number via OTP, updating user profile, changing and restoring password, etc.

## Tech Stack

- **Python 3.13**
- **FastAPI** for REST API
- **Async SQLAlchemy** for database access
- **PostgreSQL** as database
- **Pydantic** for request/response validation
- **PyJWT** for JWT handling
- **passlib (bcrypt)** for password hashing
- **Docker** for containerization

## Notes

- Access tokens are JWTs with short expiration; refresh tokens are stored hashed in the database.
- Multi-device login is supported: each device gets its own refresh token.
- Business logic (user creation, password validation, token issuance) is implemented inside the service.
- Designed for easy integration with Gateway Service and other microservices in the Microshop project.

## Running Locally

```bash
# Inside infrastructure folder
make run