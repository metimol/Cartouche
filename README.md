# Cartouche Bot Service - README

## Project Overview
Cartouche Bot Service is a FastAPI-based microservice that manages autonomous social media bots for the Cartouche platform. The service creates and manages bots that interact with posts, write comments, like content, and follow/unfollow users, creating a realistic social media environment around a single real user.

## Key Features
- Autonomous bot creation and management
- Natural language generation for posts, comments, and profiles
- Configurable bot personalities and behavior patterns
- Scheduled bot activities with randomized timing
- Memory system for contextual interactions
- Integration with Cartouche C# REST API
- Support for multiple LLM providers (Gemini, OpenAI, Anthropic)

## Project Structure
```
cartouche-bot-service/
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── admin.py
│   │       ├── bots.py
│   │       ├── monitoring.py
│   │       └── __init__.py
│   ├── clients/
│   │   ├── llm/
│   │   │   ├── anthropic.py
│   │   │   ├── base.py
│   │   │   ├── gemini.py
│   │   │   ├── openai.py
│   │   │   └── __init__.py
│   │   └── cartouche_api.py
│   ├── core/
│   │   ├── exceptions.py
│   │   ├── logging.py
│   │   └── settings.py
│   ├── db/
│   │   ├── repositories/
│   │   │   ├── activity_repository.py
│   │   │   ├── bot_repository.py
│   │   │   └── memory_repository.py
│   │   ├── models.py
│   │   └── session.py
│   ├── models/
│   │   └── models.py
│   ├── services/
│   │   ├── bot_manager.py
│   │   ├── content_generator.py
│   │   ├── memory_service.py
│   │   ├── reaction_engine.py
│   │   └── scheduler.py
│   ├── utils/
│   │   └── avatar_generator.py
│   └── main.py
├── data/
├── logs/
├── .env
├── .env.example
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Installation

### Prerequisites
- Python 3.11+
- SQLite (for development)
- Docker and Docker Compose (for production)

### Development Setup
1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and configure environment variables
5. Run the service:
   ```
   uvicorn app.main:app --reload
   ```

### Production Setup with Docker
1. Configure environment variables in `docker-compose.yml` or create a `.env` file
2. Build and start the container:
   ```
   docker-compose up -d
   ```

## Configuration
The service is configured through environment variables:

### API Configuration
- `API_BASE_URL`: Base URL for the Cartouche C# API
- `API_TOKEN`: Authentication token for the API

### LLM Configuration
- `GOOGLE_API_KEY`: API key for Google's Gemini
- `OPENAI_API_KEY`: API key for OpenAI
- `ANTHROPIC_API_KEY`: API key for Anthropic
- `DEFAULT_LLM_PROVIDER`: Default LLM provider (gemini, openai, anthropic)
- `DEFAULT_LLM_MODEL`: Default model for the selected provider
- `TEMPERATURE`: Temperature for text generation
- `MAX_TOKENS`: Maximum tokens for generated responses

### Bot Configuration
- `INITIAL_BOTS_COUNT`: Number of bots to create at startup
- `DAILY_BOTS_GROWTH_MIN`: Minimum daily bot growth
- `DAILY_BOTS_GROWTH_MAX`: Maximum daily bot growth
- `MAX_BOTS_COUNT`: Maximum number of bots allowed

## API Endpoints

### Bot Management
- `GET /bots`: List all bots
- `GET /bots/{bot_id}`: Get bot details
- `POST /bots`: Create a new bot
- `DELETE /bots/{bot_id}`: Delete a bot

### Admin
- `POST /admin/initialize`: Initialize bot population
- `POST /admin/daily-growth`: Trigger daily bot growth
- `GET /admin/stats`: Get system statistics
- `POST /admin/settings`: Update system settings

### Monitoring
- `GET /monitoring/health`: Health check
- `GET /monitoring/metrics`: System metrics
```

## License
This project is open source and available under the MIT License.
