# 🚀 Quick Start Guide

## ✅ Your API Keys Are Already Configured!

All set in your `.env` file:
- ✅ Gemini API: `AIzaSyCSEcOWpRvSt2brMRy_2Quboor34ySsrGs`
- ✅ Finnhub API: `69566abaa2fd53.94410830`
- ✅ News API: `ffdeac9cf728482ab45c49760174715e`

---

## 🎯 Start the Application (2 Options)

### Option 1: Without Database (Quick Test with Mock Data)

Perfect for testing the UI and AI agents without setting up MySQL.

**Step 1 - Update .env:**
```bash
# Change this line in .env file:
MARKET_DATA_PROVIDER=mock

# Comment out the database (add # at the start):
# DATABASE_URL=mysql+aiomysql://user:password@localhost:3306/financial_agent_db
```

**Step 2 - Run Backend:**
```bash
cd "/Users/narendrasirisipalli/Desktop/finantial agent/backend"
uvicorn app.main:app --reload
```

**Step 3 - Run Frontend (New Terminal):**
```bash
cd "/Users/narendrasirisipalli/Desktop/finantial agent/frontend"
streamlit run app.py
```

---

### Option 2: With Full Database Setup

**Step 1 - Install & Start MySQL:**

Mac (Homebrew):
```bash
brew install mysql
brew services start mysql
```

Ubuntu/Linux:
```bash
sudo apt-get install mysql-server
sudo systemctl start mysql
```

**Step 2 - Create Database:**
```bash
mysql -u root -p
# Enter your MySQL password

# Then run:
CREATE DATABASE financial_agent_db;
CREATE USER 'user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON financial_agent_db.* TO 'user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

**Step 3 - Load Schema:**
```bash
cd "/Users/narendrasirisipalli/Desktop/finantial agent"
mysql -u user -p financial_agent_db < DATABASE_SCHEMA.sql
# Password: password
```

**Step 4 - Run Backend:**
```bash
cd "/Users/narendrasirisipalli/Desktop/finantial agent/backend"
uvicorn app.main:app --reload
```

**Step 5 - Run Frontend (New Terminal):**
```bash
cd "/Users/narendrasirisipalli/Desktop/finantial agent/frontend"
streamlit run app.py
```

---

## 🌐 Access Your Application

- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 🧪 Test Without Installing MySQL (Recommended First Try)

1. Open `.env` file
2. Change line 13 to: `MARKET_DATA_PROVIDER=mock`
3. Add `#` before `DATABASE_URL` (line 2)
4. Run the backend and frontend commands
5. Visit http://localhost:8501

The mock provider will generate random stock data for testing!

---

## ❌ If You See Errors:

### "No module named 'fastapi'"
```bash
cd backend
pip install -r requirements.txt
```

### "No module named 'streamlit'"
```bash
cd frontend
pip install -r requirements.txt
```

### "Can't connect to MySQL"
- Use **Option 1** (Mock Data) above
- OR install MySQL first (see Option 2)

---

## 🎉 You're Ready!

All your API keys are configured. Just run the commands above and start analyzing stocks!
