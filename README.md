# Cartouche Bot Service (In Active Development)

## 🤖 Overview

Cartouche Bot Service is a sophisticated AI-powered social media bot simulation system built with FastAPI. It creates and manages autonomous AI bots that simulate realistic social media user behavior, including posting content, commenting, liking posts, and following/unfollowing users.

## ✨ Key Features

- **Autonomous Bot Management**: Creates and manages AI bots with unique personalities and behavior patterns
- **Natural Language Generation**: Uses LLM providers (Google Gemini, OpenAI) for realistic content creation
- **Configurable Bot Personalities**: 8 different bot categories (fan, hater, silent, random, neutral, humorous, provocative, role_player)
- **Memory System**: Vector-based memory using Qdrant for contextual bot interactions
- **Scheduled Activities**: Automated bot growth, content creation, and interaction scheduling
- **External API Integration**: Seamless integration with Cartouche C# REST API
- **Scalable Architecture**: Built with FastAPI, SQLAlchemy, and async/await patterns

## 🏗️ Architecture

```
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│   FastAPI Service   │    │   Qdrant Vector DB  │    │   External C# API   │
│                     │    │                     │    │                     │
│ • Bot Management    │◄──►│ • Bot Memory        │    │ • User Management   │
│ • Content Generation│    │ • Embeddings        │◄──►│ • Post Management   │
│ • Activity Scheduler│    │ • Similarity Search │    │ • Social Interactions│
└─────────────────────┘    └─────────────────────┘    └─────────────────────┘
           │
           ▼
┌─────────────────────┐
│    SQLite Database  │
│                     │
│ • Bot Profiles      │
│ • Activity Logs     │
│ • System Config     │
└─────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Docker & Docker Compose**: Latest versions recommended
- **LLM API Keys**: At least one of the following:
  - Google AI API key (for Gemini models)
  - OpenAI API key (for GPT models)
- **Cartouche API Access**: Valid API token for the external Cartouche service

### 1. Clone the Repository

```powershell
git clone <repository-url>
cd Cartouche
```

### 2. Environment Configuration

Create a `.env` file in the root directory:

```powershell
Copy-Item .env.example .env
```

Edit the `.env` file with your configuration:

```bash
# API Configuration
API_BASE_URL=https://fraplat.tech/mars/Cartouche
API_TOKEN=your_cartouche_api_token_here

# LLM Configuration (provide at least one)
GOOGLE_API_KEY=your_google_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
DEFAULT_LLM_PROVIDER=gemini  # or openai

# Bot Configuration
INITIAL_BOTS_COUNT=20
DAILY_BOTS_GROWTH_MIN=20
DAILY_BOTS_GROWTH_MAX=50
MAX_BOTS_COUNT=5000

# Optional: Customize other settings as needed
```

### 3. Launch the Service

```powershell
docker-compose up -d
```

### 4. Verify Installation

Check if all services are running:

```powershell
docker-compose ps
```

Access the API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Qdrant Dashboard**: http://localhost:6333/dashboard

### 5. Monitor Logs

```powershell
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f cartouche-bot-service
docker-compose logs -f qdrant
```

## 📊 API Endpoints

### Bot Management
- `GET /api/bots/` - List all bots
- `POST /api/bots/` - Create a new bot
- `GET /api/bots/{bot_id}` - Get bot details
- `DELETE /api/bots/{bot_id}` - Delete a bot

### Monitoring
- `GET /api/monitoring/stats` - Get system statistics
- `GET /api/monitoring/health` - Health check endpoint

### Root
- `GET /` - Welcome message and basic info

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `API_BASE_URL` | Cartouche API base URL | `https://fraplat.tech/mars/Cartouche` | Yes |
| `API_TOKEN` | Cartouche API authentication token | - | Yes |
| `GOOGLE_API_KEY` | Google AI API key for Gemini models | - | No* |
| `OPENAI_API_KEY` | OpenAI API key for GPT models | - | No* |
| `DEFAULT_LLM_PROVIDER` | Default LLM provider | `gemini` | Yes |
| `INITIAL_BOTS_COUNT` | Initial number of bots to create | `20` | No |
| `MAX_BOTS_COUNT` | Maximum number of bots allowed | `5000` | No |
| `LOG_LEVEL` | Logging level | `INFO` | No |

*At least one LLM API key is required.

### Bot Categories

The system supports 8 different bot personality types:

1. **Fan**: Enthusiastic, supportive, high engagement
2. **Hater**: Critical, negative, provocative comments
3. **Silent**: Observant, minimal commenting, occasional likes
4. **Random**: Unpredictable behavior patterns
5. **Neutral**: Balanced, rational, thoughtful interactions
6. **Humorous**: Meme-oriented, funny, sarcastic
7. **Provocative**: Challenging, debate-oriented
8. **Role Player**: Consistent persona-based behavior

## 🛠️ Development

### Local Development Setup

1. **Install Python 3.12+**
2. **Create virtual environment**:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
3. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```
4. **Set up environment variables**
5. **Run the development server**:
   ```powershell
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Project Structure

```
app/
├── api/                 # FastAPI routes and endpoints
├── clients/            # External API clients (Cartouche, LLM)
├── core/               # Core configuration and utilities
├── db/                 # Database models and repositories
├── models/             # Pydantic models for API
├── services/           # Business logic services
└── utils/              # Helper utilities
```

## 🐳 Docker Configuration

### Docker Compose Services

- **cartouche-bot-service**: Main FastAPI application
- **qdrant**: Vector database for bot memory system

### Volumes

- `./data`: Persistent data storage (SQLite database) and logs
- `qdrant_storage`: Qdrant vector database storage

### Networking

All services communicate through the `cartouche-network` bridge network.

## 📝 Monitoring & Logs

### Health Checks

Both services include health checks:
- **Bot Service**: HTTP health endpoint
- **Qdrant**: Built-in health endpoint

### Log Locations

- **Application Logs**: `./data/logs/cartouche.log`
- **Docker Logs**: `docker-compose logs -f`

### Metrics

Access system statistics via `/api/monitoring/stats`:
- Active bot count
- Daily activities
- Memory usage
- API response times

## 🚦 Production Deployment

### Security Considerations

1. **Use secrets management** for API keys
2. **Enable HTTPS** with reverse proxy (nginx/traefik)
3. **Set up proper firewall rules**
4. **Regular security updates**

## 📚 API Documentation

Once the service is running, comprehensive API documentation is available at:
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the application logs
3. Open an issue in the repository
4. Provide detailed error messages and logs
