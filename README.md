# claudia

Personal AI chat app powered by Anthropic Claude API.

## Stack

- **Frontend**: Next.js 14 (App Router) + Tailwind CSS
- **Backend**: FastAPI (Python)
- **Auth**: Google OAuth 2.0 + Email/Password (NextAuth.js)
- **DB**: PostgreSQL + SQLAlchemy + Alembic
- **AI**: Anthropic Claude API
- **Hosting**: GCP Compute Engine (e2-micro)

## Development

```bash
# Backend
cd backend
pip install -r requirements.txt
alembic upgrade head
uvicorn main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev
```

## Deploy (GCP)

### Prerequisites
- GCP Compute Engine instance (e2-micro, Debian/Ubuntu)
- DNS: `claudia.soushu.biz` → instance static IP

### Steps

```bash
# 1. Clone repo on GCP instance
git clone <repo-url> ~/claudia
cd ~/claudia

# 2. Create .env files
cp .env.example .env          # edit with production values
cp frontend/.env.example frontend/.env.local  # edit with production values

# 3. Run setup script
bash deploy/setup.sh
```

The setup script handles: PostgreSQL, Python venv, Node.js, npm build, Alembic migrations, systemd services, Nginx, and SSL (certbot).

### Service Management

```bash
sudo systemctl status claudia-backend claudia-frontend
sudo systemctl restart claudia-backend
sudo journalctl -u claudia-backend -f   # view logs
```
