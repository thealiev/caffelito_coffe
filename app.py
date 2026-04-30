from flask import Flask
from supabase import create_client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set in .env file")

supabase = create_client(supabase_url, supabase_key)

@app.route('/')
def home():
    """Test endpoint to verify Supabase connection"""
    try:
        # Test connection by checking server info
        result = supabase.table('_test_connection').select('*').limit(1).execute()
        
        return {
            "status": "success",
            "message": "Supabase connection working!",
            "data": result.data if result.data else "No test data found"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": "Supabase connection failed",
            "error": str(e)
        }

@app.route('/health')
def health():
    """Simple health check endpoint"""
    return {"status": "healthy", "service": "caffelito_bot"}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
