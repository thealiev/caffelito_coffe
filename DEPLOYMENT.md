# Caffelito Bot Deployment Guide

## 🚀 Quick Deployment Options

### Option 1: Railway (Easiest)
1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway**
   ```bash
   railway login
   ```

3. **Deploy**
   ```bash
   railway init
   railway up
   ```

4. **Set Environment Variables** in Railway dashboard:
   ```
   SUPABASE_URL=https://wjknmixoxdbgvqwperlm.supabase.co
   SUPABASE_KEY=sb_publishable_xrFyDdY6AIsNqDeSqW3M0A_e5_il07U
   FLASK_DEBUG=False
   FLASK_SECRET_KEY=your-secret-key-here
   ```

### Option 2: Heroku
1. **Install Heroku CLI**
2. **Create app**
   ```bash
   heroku create your-app-name
   ```

3. **Set environment variables**
   ```bash
   heroku config:set SUPABASE_URL=https://wjknmixoxdbgvqwperlm.supabase.co
   heroku config:set SUPABASE_KEY=sb_publishable_xrFyDdY6AIsNqDeSqW3M0A_e5_il07U
   heroku config:set FLASK_DEBUG=False
   heroku config:set FLASK_SECRET_KEY=your-secret-key-here
   ```

4. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy caffelito bot"
   git push heroku main
   ```

### Option 3: VPS/Docker
1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.14-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 5000
   CMD ["python", "-m", "waitress", "--host=0.0.0.0", "--port=5000", "app_production:app"]
   ```

2. **Build and run**
   ```bash
   docker build -t caffelito-bot .
   docker run -p 5000:5000 caffelito-bot
   ```

## 📋 Prerequisites

### 1. Set up Supabase Database
Create a `todos` table in your Supabase dashboard:

```sql
CREATE TABLE todos (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### 2. Environment Variables
Create `.env` file with:
```
SUPABASE_URL=https://wjknmixoxdbgvqwperlm.supabase.co
SUPABASE_KEY=sb_publishable_xrFyDdY6AIsNqDeSqW3M0A_e5_il07U
FLASK_DEBUG=False
FLASK_SECRET_KEY=your-production-secret-key
PORT=5000
```

## 🔧 Local Testing

### Test with Waitress (Production Server)
```bash
python -m waitress --host=0.0.0.0 --port=5000 app_production:app
```

### Test with Flask Dev Server
```bash
python app_production.py
```

## 📱 Access Points

Once deployed, your app will have these endpoints:

- **Main App**: `https://your-domain.com/`
- **Health Check**: `https://your-domain.com/health`
- **API**: `https://your-domain.com/api/todos`

## 🛡️ Security Notes

1. **Change FLASK_SECRET_KEY** - Generate a secure random key
2. **Use service_role key** for backend operations if needed
3. **Enable RLS** on Supabase tables for security
4. **Use HTTPS** in production

## 🐛 Troubleshooting

### Common Issues:
- **Module not found**: Run `pip install -r requirements.txt`
- **Connection errors**: Check Supabase URL and key
- **Permission denied**: Ensure API key has correct permissions
- **Port conflicts**: Change PORT in environment variables

### Logs:
Check application logs for debugging:
```bash
# Local testing
python app_production.py

# Production logs vary by platform
# Railway: railway logs
# Heroku: heroku logs --tail
```

## 📞 Support

For issues:
1. Check Supabase dashboard for database status
2. Verify environment variables
3. Check platform-specific logs
4. Test locally first before deploying
