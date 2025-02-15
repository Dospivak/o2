# Membership Management System

A Flask-based web application for managing gym memberships.

## Features

- Add new members
- View member information
- List available packages
- Calculate package prices

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── routes/
│   ├── models/
│   └── services/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── templates/
├── tests/
├── config/
├── .env
├── requirements.txt
└── README.md
```

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Update the values in `.env` as needed

4. Run the application:
   ```bash
   flask run
   ```

## Development

- The application uses Flask for the web framework
- Templates are in the `templates` directory
- Static files (CSS, JS, images) go in the `static` directory
- Configuration is managed through environment variables
- Business logic is in the `app/services` directory
- Database models are in the `app/models` directory

## Testing

Run tests with:
```bash
python -m pytest
``` 