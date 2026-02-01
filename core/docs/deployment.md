# Deployment

Deploying the Music API is simple thanks to Docker.

## Docker Compose

The easiest way to run the entire stack (API, Dashboard, and Documentation) is using Docker Compose.

```bash
docker compose up -d --build
```

### Services

| Service | internal Port | External Port | URL |
| --- | --- | --- | --- |
| **API** | 5001 | 5001 | `http://localhost:5001` |
| **Dashboard** | 5001 | 5002 | `http://localhost:5002` |
| **Docs** | 8000 | 5003 | `http://localhost:5003` |

---

## Configuration

You can customize the deployment using environment variables in `.env`:

```env
API_URL=http://localhost:5001
DASHBOARD_URL=http://localhost:5002
API_DOCS_URL=http://localhost:5003
```
