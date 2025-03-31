# Shopping List Web Application

A Dockerized Flask web application for managing shopping lists, optimized for both ARM64 and x86 architectures.

## Features

- 📝 Create and manage shopping lists
- ✅ Interactive checkboxes with persistent state
- 📅 Organized by date (year/month/day)
- 📱 Mobile-friendly interface
- 🐳 Docker container support

## Prerequisites

- Docker Engine (v20.10+)
- Docker Compose (v2.0+)
- Python 3.9+ (for local development)

## Build and run

1. Clone repository and navigate to its directory
2. Optionally create `.env` file to store environment variables
   ```
   APP_PORT=5000                # Host port to expose
   FLASK_ENV=production         # production/development mode
   SECRET_KEY=your_secret_key   # Flask secret key
   ```
3. Deploy with docker-compose:
   ```
   docker-compose up -d --build
   ```

## Usage
Access the application at:
```
http://localhost:5000
```
or
```
http://<your_ip_address>:<APP_PORT>
```

**Key Functions:**
- Create New List: Add items individually or paste multiple at once
- Edit Lists: Modify existing lists or change dates
- Check Items: Persistent checkbox states
- Delete Lists: Full list removal

For adding multiple entries a string with comma-separated (default delimeter, can be changed) values can pasted in text field, then just press `Save list`.

## Database
The application uses SQLite stored in `database/shopping_lists.db`. For Docker, this is persisted via volume.

## Running Without Docker
```
python -m venv venv
source venv/bin/activate        # Linux/Mac
source venv/Scripts/activate    # Windows (Bash)
pip install -r requirements.txt
python run.py
```

## Authentication
The application supports simple single user authentication.

The default credentials are `admin`/`admin` for username and password.

They can be changed by adding `AUTH_USERNAME` and `AUTH_PASSWORD` variables in `.env` file in the root directory.