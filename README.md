# Social Network

A social network project built with Django.

## Features

- User authentication
- User profiles
- Posts and comments
- Social network functionalities

## Requirements

- Python 3.x
- PostgreSQL

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
```

### 2. Create virtual environment

```bash
python -m venv venv
```

Activate virtual environment:

Windows:

```bash
venv\Scripts\activate
```

Linux / macOS:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment variables

Create a `.env` file in the root directory and add required variables:

```env
SECRET_KEY=your-secret-key

DEBUG=True

DB_NAME=your-database-name
DB_USER=your-database-user
DB_PASSWORD=your-database-password
DB_HOST=localhost
DB_PORT=5432
```

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Run development server

```bash
python manage.py runserver
```

The project will be available at:

```
http://127.0.0.1:8000/
```

## Project Structure

```
Social_Network/
│
├── apps/
├── config/
├── manage.py
├── requirements.txt
├── .env
├── .env.example
└── README.md
```

## Technologies

- Python
- Django
- PostgreSQL
- Django-environ