# Movie Recommendation System (Server-Client Architecture)

This project implements a movie recommendation system using a client-server architecture with FastAPI for the backend server and PyQt5 for the frontend client.

## System Architecture

- **Server**: FastAPI application that provides movie data and recommendations
- **Client**: PyQt5 desktop application that fetches and displays data from the server

## Prerequisites

- Python 3.7+
- FastAPI
- Uvicorn
- PyQt5
- Requests

## Installation

1. Install the required dependencies:

```bash
pip install fastapi uvicorn pydantic PyQt5 requests
```

## Running the Application

### Step 1: Start the Server

```bash
python server.py
```

The server will start running at `http://127.0.0.1:8000`.

### Step 2: Launch the Client

```bash
python client.py
```

The PyQt5 client application will start and connect to the server.

## API Endpoints

The server exposes the following API endpoints:

- `GET /users` - Get a list of all available user IDs
- `GET /user/{user_id}/movies` - Get favorite movies for a specific user
- `POST /recommendations` - Get movie recommendations based on user ID and count

## Features

- List of users loaded from the server
- User's favorite movies retrieved from the server
- Configurable number of movie recommendations
- Error handling for server connection issues
- Loading indicators for async operations

## Extending the System

To extend this system:
- Add a real recommendation algorithm on the server
- Implement user authentication
- Add a database instead of in-memory storage
- Support for adding/editing user movie preferences

## License

This project is for educational purposes.