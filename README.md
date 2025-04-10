
# AI-Driven Website Builder

An intelligent website builder that uses AI (Google Gemini) to generate customized website content and templates based on user inputs.

## Features

- **AI-Powered Content Generation**: Utilizes Google Gemini API to generate tailored website content
- **Multiple Templates**: Supports various website templates (Basic, Business, Portfolio)
- **Dashboard Interface**: User-friendly dashboard for managing websites
- **Preview Engine**: Real-time website preview functionality
- **Authentication System**: Secure user authentication and authorization
- **REST API**: Complete API endpoints for website management

## Project Structure

```
├── authentication/         # User authentication module
├── preview_engine/        # Website preview and template rendering
├── website_generator/     # AI-based content generation
├── website_manager/       # Website management and storage
├── utils/                 # Utility functions and helpers
└── templates/            # HTML templates
```

## Setup

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r dependencies.txt
   ```
3. Configure your Gemini API key in settings
4. Run migrations:
   ```
   python manage.py migrate
   ```
5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```
6. Start the development server:
   ```
   python manage.py runserver 0.0.0.0:8000
   ```

## API Endpoints

- `/api/auth/` - Authentication endpoints
- `/api/websites/` - Website management
- `/api/generator/` - Content generation
- `/api/preview/` - Website preview

## Technology Stack

- Backend: Django/Python
- Database: SQLite
- AI: Google Gemini API
- Frontend: HTML/CSS/JavaScript

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request


