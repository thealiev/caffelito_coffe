import os
import logging
from flask import Flask, jsonify
from supabase import create_client, Client
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Production configuration
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-change-in-production')

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    logger.error("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
    raise RuntimeError("Missing required Supabase configuration")

try:
    supabase: Client = create_client(supabase_url, supabase_key)
    logger.info("Supabase client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Supabase client: {e}")
    raise

@app.route('/')
def index():
    """Get all todos from Supabase"""
    try:
        logger.info("Fetching todos from Supabase")
        response = supabase.table('todos').select("*").execute()
        
        if response.data is None:
            logger.warning("No data returned from Supabase")
            todos = []
        else:
            todos = response.data
            logger.info(f"Retrieved {len(todos)} todos")

        html = '<h1>Caffelito Bot - Todos</h1><ul>'
        for todo in todos:
            html += f'<li>{todo.get("name", "Unnamed todo")}</li>'
        html += '</ul>'
        
        return html

    except Exception as e:
        logger.error(f"Error fetching todos: {e}")
        return jsonify({
            "error": "Failed to fetch todos",
            "message": str(e)
        }), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "caffelito_bot",
        "version": "1.0.0"
    })

@app.route('/api/todos')
def api_todos():
    """API endpoint for todos"""
    try:
        response = supabase.table('todos').select("*").execute()
        return jsonify({
            "status": "success",
            "data": response.data or [],
            "count": len(response.data) if response.data else 0
        })
    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    logger.warning(f"404 error: {error}")
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"500 error: {error}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    logger.info("Starting Caffelito Bot application")
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=app.config['DEBUG']
    )
