# 🪟 Financial AI Agent Platform - Windows Setup Guide

## ⚡ Quick Start (5 Minutes)

### Prerequisites
1. **Docker Desktop for Windows** - [Download Here](https://www.docker.com/products/docker-desktop/)
2. **Git for Windows** - [Download Here](https://git-scm.com/download/win)
3. **Text Editor** - VS Code, Notepad++, or any editor

---

## 📥 Step 1: Clone the Repository

Open **PowerShell** or **Command Prompt** and run:

```powershell
# Clone the repository
git clone <YOUR_REPOSITORY_URL>
cd financial_ai_agent

# OR if you downloaded as ZIP
# Extract the ZIP file and open PowerShell in that folder
```

---

## 🔧 Step 2: Setup Environment Variables

### Option A: Using PowerShell (Recommended)

```powershell
# Copy the example file
copy .env.example .env

# Edit the .env file
notepad .env
```

### Option B: Using Command Prompt

```cmd
copy .env.example .env
notepad .env
```

### ✏️ Edit the `.env` file with your API keys:

```env
# Database Configuration
DATABASE_URL=sqlite+aiosqlite:///./test.db

# Security (Generate a random string for production)
SECRET_KEY=your-secret-key-here-change-this-to-random-string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Gemini API (Get from: https://makersuite.google.com/app/apikey)
GEMINI_API_KEY=your-gemini-api-key-here

# Finnhub API (Get from: https://finnhub.io/register)
MARKET_DATA_API_KEY=your-finnhub-api-key-here

# News API (Get from: https://newsapi.org/register)
NEWS_API_KEY=your-news-api-key-here

# Application
ENVIRONMENT=development
DEBUG=True
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:8501
```

**🔑 Where to Get API Keys (All FREE):**
1. **Gemini API**: https://makersuite.google.com/app/apikey
2. **Finnhub API**: https://finnhub.io/register
3. **News API**: https://newsapi.org/register

---

## 🐳 Step 3: Start Docker Desktop

1. Open **Docker Desktop**
2. Wait until Docker is running (green icon in system tray)
3. Make sure it says "Docker Desktop is running"

---

## 🚀 Step 4: Run the Application

### Using PowerShell:

```powershell
# Make sure you're in the project directory
cd path\to\financial_ai_agent

# Start the application
docker-compose up -d

# Check if containers are running
docker-compose ps

# View logs (optional)
docker-compose logs -f
```

### Using Command Prompt:

```cmd
cd path\to\financial_ai_agent
docker-compose up -d
docker-compose ps
```

**Expected Output:**
```
NAME                       STATUS          PORTS
financial_agent_backend    Up X seconds    0.0.0.0:8000->8000/tcp
financial_agent_frontend   Up X seconds    0.0.0.0:8501->8501/tcp
```

---

## 🌐 Step 5: Access the Application

Open your web browser and go to:

- **Frontend (User Interface):** http://localhost:8501
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

---

## 🎯 Step 6: Test the Application

1. **Open Frontend:** http://localhost:8501
2. **Sign Up:**
   - Email: test@example.com
   - Username: testuser
   - Password: Test12345
   - Full Name: Test User
3. **Login** with your credentials
4. **Go to "AI Insights" tab**
5. **Enter a stock ticker:** AAPL (or GOOGL, MSFT, TSLA)
6. **Click "Analyze"**
7. **Get AI analysis in 3-5 seconds!**

---

## 🛑 Stop the Application

```powershell
docker-compose down
```

---

## 🔄 Restart the Application

```powershell
docker-compose restart
```

---

## 🐛 Troubleshooting

### ❌ Problem: "Port 8000 or 8501 is already in use"

**Solution 1: Find and stop the process**

PowerShell:
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with the number from above)
taskkill /PID <PID> /F

# Do the same for port 8501
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

**Solution 2: Change ports in `docker-compose.yml`**

Edit `docker-compose.yml` and change:
```yaml
ports:
  - "8080:8000"  # Changed from 8000:8000
```

Then access at http://localhost:8080

---

### ❌ Problem: "Docker is not running"

**Solution:**
1. Open Docker Desktop application
2. Wait for it to fully start (green icon in tray)
3. Try the docker-compose command again

---

### ❌ Problem: "docker-compose command not found"

**Solution:**

Try using `docker compose` (with a space) instead:
```powershell
docker compose up -d
docker compose down
docker compose ps
```

---

### ❌ Problem: "Permission denied" or "Access is denied"

**Solution:**
1. Run PowerShell as Administrator
2. Right-click PowerShell → "Run as administrator"
3. Try the commands again

---

### ❌ Problem: Backend shows "API quota exceeded" or errors

**Solution:**
1. Check your API keys in `.env` file
2. Make sure Gemini API key is valid
3. Check Finnhub API quota at https://finnhub.io/dashboard
4. News API has a limit of 100 requests/day on free tier

---

### ❌ Problem: Frontend can't connect to backend

**Solution:**
1. Check if backend is running: `docker-compose ps`
2. Check backend logs: `docker-compose logs backend`
3. Make sure port 8000 is not blocked by firewall
4. Try accessing: http://localhost:8000/health

---

### ❌ Problem: Containers keep restarting

**Solution:**
```powershell
# Stop everything
docker-compose down

# Remove all containers
docker-compose rm -f

# Rebuild and start
docker-compose build --no-cache
docker-compose up -d

# Check logs for errors
docker-compose logs -f
```

---

## 📊 Useful Commands

### View Logs
```powershell
# All logs
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# Frontend only
docker-compose logs -f frontend

# Last 50 lines
docker-compose logs --tail=50
```

### Check Container Status
```powershell
docker-compose ps
docker ps
```

### Restart Services
```powershell
# Restart all
docker-compose restart

# Restart backend only
docker-compose restart backend

# Restart frontend only
docker-compose restart frontend
```

### Clean Up Everything
```powershell
# Stop and remove containers
docker-compose down

# Remove containers and volumes
docker-compose down -v

# Remove everything including images
docker-compose down --rmi all -v
```

---

## 🔒 Windows Firewall

If you get firewall prompts:
1. Click **"Allow access"** for Docker
2. Allow both Private and Public networks
3. If blocked, go to Windows Firewall settings and allow Docker

---

## 📁 File Structure

```
financial_ai_agent/
├── backend/                 # Backend API code
├── frontend/               # Frontend UI code
├── docker-compose.yml      # Docker configuration
├── .env                    # Your environment variables (DO NOT COMMIT)
├── .env.example           # Example environment file
├── README.md              # Main documentation
└── WINDOWS_SETUP_GUIDE.md # This file
```

---

## 🎓 For Development

### Access Container Shell

```powershell
# Backend container
docker exec -it financial_agent_backend bash

# Frontend container
docker exec -it financial_agent_frontend bash
```

### View Database

The SQLite database is at `backend/test.db`. You can view it with:
- [DB Browser for SQLite](https://sqlitebrowser.org/)
- Or access via backend container

---

## 🚀 Performance Tips

1. **Allocate more resources to Docker:**
   - Open Docker Desktop
   - Go to Settings → Resources
   - Increase CPU and Memory if needed

2. **Use WSL 2 backend (recommended):**
   - Docker Desktop → Settings → General
   - Enable "Use the WSL 2 based engine"

3. **Close unnecessary applications:**
   - Free up ports 8000 and 8501
   - Close other Docker containers

---

## 📞 Common Questions

**Q: Can I use a different port?**
A: Yes, edit `docker-compose.yml` and change the port mappings.

**Q: How do I update the code?**
A: Run `git pull` then `docker-compose restart`

**Q: Where is the data stored?**
A: SQLite database is in `backend/test.db`

**Q: Can I deploy this to production?**
A: Yes, but change SECRET_KEY and set DEBUG=False

**Q: How do I backup my data?**
A: Copy the `backend/test.db` file

---

## ✅ Success Checklist

- [ ] Docker Desktop installed and running
- [ ] Repository cloned/downloaded
- [ ] `.env` file created with valid API keys
- [ ] `docker-compose up -d` completed successfully
- [ ] Can access http://localhost:8501
- [ ] Can access http://localhost:8000
- [ ] Can sign up and login
- [ ] Can get AI analysis results

---

## 🎉 Congratulations!

Your Financial AI Agent Platform is now running on Windows!

**Need Help?**
- Check the logs: `docker-compose logs -f`
- Check container status: `docker-compose ps`
- Restart: `docker-compose restart`

**Enjoy your AI-powered financial analysis platform!** 📈

---

*Last Updated: January 5, 2026*
*For: Windows 10/11 with Docker Desktop*
