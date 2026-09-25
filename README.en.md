# My Media Site

This is a media resource management website developed based on the Django framework, used to display and manage collections of videos and audio.

## Project Introduction

My Media Site provides a streamlined media resource management platform that supports categorized display of video and audio content. Users can browse different media collections via the web interface and view detailed information about videos and audio.

## Tech Stack

- **Backend**: Django 4.x
- **Frontend**: HTML/CSS/JavaScript
- **Database**: SQLite (Default)

## Project Structure

```
my_media_site/
├── manage.py              # Django management script
├── my_media_site/         # Project main directory
│   ├── settings.py        # Project configuration
│   ├── urls.py            # URL routing configuration
│   ├── wsgi.py            # WSGI configuration
│   └── asgi.py            # ASGI configuration
└── player/                # Media playback application
    ├── models.py          # Data models
    ├── views.py           # View functions
    ├── urls.py            # App routes
    ├── admin.py           # Admin panel configuration
    └── templates/         # Template files
```

## Data Models

The project includes the following core models:

- **Collection**: Media collection, used for grouping and managing videos and audio
- **Video**: Video resource, stores video title, description, file path, etc.
- **Audio**: Audio resource, stores audio title, description, file path, etc.

## Features

- Media collection categorization and management
- Video resource display
- Audio resource display
- Django admin panel integration
- Responsive web design

## Quick Start

### Environment Requirements

- Python 3.8+
- Django 4.x

### Installation Steps

1. Clone the project locally

```bash
git clone https://gitee.com/xiaotu20/my_media_site.git
cd my_media_site
```

2. Create a virtual environment (optional)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

3. Install dependencies

```bash
pip install django
```

4. Run database migrations

```bash
python manage.py migrate
```

5. Create an admin account

```bash
python manage.py createsuperuser
```

6. Start the development server

```bash
python manage.py runserver
```

7. Access the application

- Website Homepage: http://127.0.0.1:8000/
- Admin Panel: http://127.0.0.1:8000/admin/

## Usage Instructions

### Admin Backend

1. Log in to the admin backend to create Collections
2. Add Video and Audio resources to the collections
3. Fill in relevant titles, descriptions, and file paths

### Frontend Display

Visit the website homepage to view all media resources and collection lists.

## Development Guide

### Running Tests

```bash
python manage.py test
```

### Creating an Application

To extend functionality, you can create a new Django application:

```bash
python manage.py startapp new_app
```

## License

This project is for learning and reference purposes only.