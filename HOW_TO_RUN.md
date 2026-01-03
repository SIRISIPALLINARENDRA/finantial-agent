# 🚀 How to Run Your Financial AI Platform

## ✅ News API Status: WORKING PERFECTLY!

**Test Result:**
- ✅ Status: OK
- ✅ Articles Found: 338 for AAPL
- ✅ Sample: "Apple names Amar Subramanya new VP of AI..."

**Your News API is ready!** 🎉

---

## 📋 Quick Start (2 Steps)

### Step 1: Backend is Already Running ✅

Your backend is **already running** on port 8000!

**Check it:** http://127.0.0.1:8000/health

If you need to restart it:
```bash
cd "/Users/narendrasirisipalli/Desktop/finantial agent/backend"
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

---

### Step 2: Start Frontend

**Open a NEW terminal window and run:**

```bash
cd "/Users/narendrasirisipalli/Desktop/finantial agent/frontend"
python3 -m pip install -r requirements.txt
python3 -m streamlit run app.py
```

**That's it!** The frontend will open automatically at **http://localhost:8501**

---

## 🔐 Login

**Username:** `testuser`
**Password:** `testpass123`

Or click "Sign Up" to create your own account!

---

## 📊 What You'll Get

### 1. **Dashboard** 📈
- Real-time stock prices (from Finnhub)
- Live price updates
- Track multiple stocks
- Auto-refresh

### 2. **AI Insights** 🤖
- Powered by Google Gemini
- 4 specialized AI agents:
  - Market Data Analyst
  - News & Sentiment Analyst
  - Risk & ESG Analyst
  - Decision Synthesis Coordinator
- Real financial news analysis
- Risk assessment

### 3. **Watchlist** ⭐
- Save your favorite stocks
- Add custom notes
- Track what matters to you

### 4. **History** 📜
- View past AI analyses
- Track your queries
- Review insights

---

## 🔧 Troubleshooting

### If Frontend Won't Start:

**Install dependencies:**
```bash
cd "/Users/narendrasirisipalli/Desktop/finantial agent/frontend"
pip3 install streamlit requests pandas
```

### If Backend Stopped:

**Restart it:**
```bash
cd "/Users/narendrasirisipalli/Desktop/finantial agent/backend"
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### If You See "Connection Error":

Make sure backend is running! Check: http://127.0.0.1:8000/health

---

## 🎯 Complete Workflow

**Terminal 1 (Backend):**
```bash
cd "/Users/narendrasirisipalli/Desktop/finantial agent/backend"
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

**Terminal 2 (Frontend):**
```bash
cd "/Users/narendrasirisipalli/Desktop/finantial agent/frontend"
python3 -m streamlit run app.py
```

**Browser:**
- Open: http://localhost:8501
- Login: testuser / testpass123
- Start analyzing stocks!

---

## ✅ What's Working

| Feature | Status | Details |
|---------|--------|---------|
| Backend | ✅ Running | Port 8000 |
| Real-Time Stock Data | ✅ Working | Finnhub API |
| News API | ✅ Working | 338 articles fetched |
| AI Agents | ✅ Ready | Google Gemini |
| Authentication | ✅ Working | JWT Tokens |
| Database | ✅ Connected | SQLite |

---

## 🎉 You're Ready!

**Just run the frontend and enjoy your AI-powered financial platform!**

All data is REAL:
- Stock prices: Live from Finnhub ✅
- News: Real financial news ✅
- AI Analysis: Powered by Gemini ✅
