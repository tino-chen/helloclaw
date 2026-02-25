# HelloClaw Backend

AI Agent powered by HelloAgents framework.

## Development

```bash
# Install dependencies
uv sync

# Run development server
uv run uvicorn main:app --reload --port 8000
```

## API Endpoints

- `GET /health` - Health check
- `POST /api/chat/send` - Send chat message
- `GET /api/session/list` - List sessions
- `POST /api/session/create` - Create session
- `GET /api/config/list` - List config files
- `GET /api/config/{name}` - Get config file
- `PUT /api/config/{name}` - Update config file
