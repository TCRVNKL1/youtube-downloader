# YouTube Downloader - Development Guide

## Overview

This project is a web application for downloading YouTube videos in various formats and quality options. It's built with Flask and uses yt-dlp to handle YouTube video extraction and downloading. The application allows users to enter a YouTube URL, displays video information, and provides download options.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The YouTube Downloader follows a simple web application architecture:

- **Frontend**: HTML templates with Bootstrap for styling, JavaScript for interactivity
- **Backend**: Flask Python application
- **Video Processing**: yt-dlp library for video information extraction and downloading
- **Temporary Storage**: Local file system for storing videos before serving to users

The application is designed to be deployed on Replit's autoscaling infrastructure using Gunicorn as the WSGI server.

## Key Components

### Backend Components

1. **Flask Application** (`app.py`)
   - Creates and configures the Flask application
   - Sets up logging and temporary storage directory for downloads

2. **Routes** (`routes.py`)
   - Defines HTTP endpoints for the application:
     - `/`: Main landing page
     - `/validate-url`: API endpoint to validate and fetch YouTube video info
     - `/download-options`: Page showing available download formats

3. **Utilities** (`utils.py`)
   - Helper functions for YouTube-related operations:
     - URL validation
     - Video ID extraction
     - Data formatting

### Frontend Components

1. **Templates** (`templates/`)
   - `layout.html`: Base template with common elements (navbar, styling)
   - `index.html`: Home page with YouTube URL input form
   - `download.html`: Shows video information and download options
   - `error.html`: Error page for displaying issues

2. **Static Files** (`static/`)
   - JavaScript (`js/`):
     - `script.js`: Main application logic
     - `ads.js`: Ad management functionality
   - CSS (`css/`):
     - `style.css`: Custom styling for the application

## Data Flow

1. **Video Information Retrieval**:
   - User enters a YouTube URL on the home page
   - Frontend sends URL to `/validate-url` endpoint
   - Backend validates URL format and uses yt-dlp to fetch video metadata
   - Video information is stored in session and returned to frontend
   - Frontend displays video details and navigates to download options

2. **Video Download Process**:
   - User selects desired format and quality on download page
   - Backend uses yt-dlp to download the video in the requested format
   - Video is temporarily stored in the `temp_downloads` directory
   - File is served to the user for download
   - Temporary file is cleaned up afterward

## External Dependencies

### Python Packages

- **Flask**: Web framework for the application
- **yt-dlp**: YouTube video metadata extraction and downloading
- **gunicorn**: WSGI HTTP server for running the application
- **Werkzeug**: WSGI utility library used by Flask
- **Flask-SQLAlchemy**: ORM for database operations (not yet implemented)
- **psycopg2-binary**: PostgreSQL adapter (not yet implemented)
- **email-validator**: For validation in future user account features

### Frontend Libraries (CDN)

- **Bootstrap**: CSS framework for responsive design
- **Font Awesome**: Icon library
- **Google Fonts**: Web fonts for typography

## Deployment Strategy

The application is configured for deployment on Replit's autoscaling infrastructure:

- **Web Server**: Gunicorn WSGI server
- **Command**: `gunicorn --bind 0.0.0.0:5000 main:app`
- **Environment**: Python 3.11 with PostgreSQL support

### Development Workflow

The `.replit` file configures the development environment with:
- Nix packages for system dependencies (OpenSSL, PostgreSQL)
- A run button workflow that starts the application with hot-reload support
- Port configuration to expose the web server

### Future Considerations

1. **Database Implementation**:
   - SQLAlchemy is included in dependencies for future database features
   - PostgreSQL adapter is available for data persistence

2. **User Accounts**:
   - Email validation dependency suggests plans for user registration

3. **Performance Optimization**:
   - Consider implementing caching for frequently accessed videos
   - Add background job processing for heavy download tasks