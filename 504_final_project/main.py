import json
import os
import flask
from sqlalchemy import create_engine, text
from huggingface_hub import InferenceClient
from PyPDF2 import PdfReader
from dotenv import load_dotenv

load_dotenv()

app = flask.Flask(__name__)

# Load HTML template - will be loaded on first request
HTML_TEMPLATE = None

def load_template():
    """Load HTML template from file"""
    global HTML_TEMPLATE
    
    if HTML_TEMPLATE is not None:
        return HTML_TEMPLATE
    
    # Try reading from disk with multiple fallback paths
    possible_paths = [
        '/app/index.html',           # Docker container WORKDIR
        'index.html',                 # Current directory
        os.path.join(os.path.dirname(__file__), 'index.html'),  # Relative to this file
    ]
    
    print(f"[TEMPLATE DEBUG] Starting template load. CWD: {os.getcwd()}, __file__: {__file__}")
    
    for template_path in possible_paths:
        print(f"[TEMPLATE DEBUG] Checking path: {template_path}")
        try:
            if os.path.exists(template_path):
                print(f"[TEMPLATE DEBUG] File exists at {template_path}, attempting to read...")
                with open(template_path, 'r', encoding='utf-8') as f:
                    HTML_TEMPLATE = f.read()
                    print(f"[TEMPLATE] ✓ Successfully loaded from: {template_path} ({len(HTML_TEMPLATE)} bytes)")
                    return HTML_TEMPLATE
            else:
                print(f"[TEMPLATE DEBUG] File does NOT exist at {template_path}")
        except Exception as e:
            print(f"[TEMPLATE DEBUG] Exception reading {template_path}: {type(e).__name__}: {e}")
    
    # If file not found, log details and return error
    print(f"[TEMPLATE ERROR] ✗ Could not find index.html in any of these paths: {possible_paths}")
    try:
        print(f"[TEMPLATE DEBUG] Current working directory: {os.getcwd()}")
        print(f"[TEMPLATE DEBUG] __file__ location: {__file__}")
        if os.path.exists('/app'):
            print(f"[TEMPLATE DEBUG] Files in /app: {os.listdir('/app')}")
        else:
            print(f"[TEMPLATE DEBUG] /app directory does not exist")
        print(f"[TEMPLATE DEBUG] Files in cwd: {os.listdir(os.getcwd())}")
    except Exception as debug_err:
        print(f"[TEMPLATE DEBUG] Error during debug info collection: {debug_err}")
    
    return "<h1>Error loading template</h1>"

@app.route('/')
def index():
    template = load_template()
    return template

# Global clients (lazy initialization)
db_engine = None
hf_client = None

def get_db_engine():
    """Initialize database connection lazily"""
    global db_engine
    if db_engine is None:
        sql_username = os.getenv("DB_APP_USERNAME")
        sql_password = os.getenv("DB_APP_PASSWORD")
        sql_database = os.getenv("DB_DATABASE")
        sql_hostname = os.getenv("DB_HOSTNAME")
        sql_port = os.getenv("DB_PORT", "3306")
        
        if all([sql_username, sql_password, sql_hostname, sql_database]):
            try:
                server_url = f"mysql+pymysql://{sql_username}:{sql_password}@{sql_hostname}:{sql_port}/{sql_database}"
                db_engine = create_engine(server_url, pool_pre_ping=True, connect_args={"ssl": {"ssl": True, "check_hostname": False, "ca": None}})
                with db_engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
                    print("[DB] Database connection successful")
            except Exception as e:
                print(f"[DB ERROR] {e}")
                db_engine = None
    return db_engine

def get_hf_client():
    """Initialize Hugging Face client lazily"""
    global hf_client
    if hf_client is None:
        hf_api_key = os.getenv("HUGGINGFACE_API_KEY")
        print(f"[HF DEBUG] Reading HUGGINGFACE_API_KEY from environment: {hf_api_key[:20] if hf_api_key else 'NOT SET'}...")
        if hf_api_key:
            try:
                hf_client = InferenceClient(api_key=hf_api_key)
                print("[HF] Hugging Face client initialized successfully")
            except Exception as e:
                print(f"[HF ERROR] Failed to initialize: {e}")
        else:
            print("[HF WARNING] HUGGINGFACE_API_KEY not found in environment variables")
    return hf_client

def extract_pdf_from_folder():
    """Load and extract text from first PDF in data folder"""
    try:
        data_folder = "data"
        if not os.path.exists(data_folder):
            return ""
        
        for filename in os.listdir(data_folder):
            if filename.lower().endswith('.pdf'):
                filepath = os.path.join(data_folder, filename)
                with open(filepath, 'rb') as file:
                    reader = PdfReader(file)
                    text = ""
                    for page in reader.pages[:3]:  # First 3 pages only
                        text += page.extract_text()
                    return text[:2000]  # First 2000 chars
    except Exception as e:
        print(f"[PDF ERROR] {e}")
    return ""


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint - responds immediately without initialization"""
    return {"status": "ok"}, 200

@app.route("/api/inquire", methods=["POST"])
def process_inquiry():
    """Process user inquiry with PDF context and AI response"""
    try:
        data = flask.request.get_json() or {}
        user_name = data.get("user_name", "Anonymous")
        user_inquiry = data.get("user_inquiry", "")
        
        if not user_inquiry:
            return {"error": "user_inquiry is required"}, 400
        
        # Load PDF context
        pdf_context = extract_pdf_from_folder()
        
        # Get AI response
        hf = get_hf_client()
        ai_response = ""
        response_source = "unknown"
        
        if hf:
            try:
                # Create prompt with PDF context
                if pdf_context:
                    prompt = f"""Context from document:
{pdf_context}

User Question: {user_inquiry}

Answer:"""
                else:
                    prompt = user_inquiry
                
                response = hf.text_generation(
                    model="gpt2",
                    prompt=prompt,
                    max_new_tokens=200
                )
                ai_response = response
                response_source = "hugging_face"
            except Exception as e:
                ai_response = f"AI Error: {str(e)}"
                response_source = "error"
        else:
            # Fallback: Search all 3 tables for related information
            engine = get_db_engine()
            if engine:
                try:
                    with engine.connect() as conn:
                        # Search SAVED_RESPONSES for similar inquiries
                        saved_result = conn.execute(text("""
                            SELECT ResponseData FROM SAVED_RESPONSES 
                            WHERE LOWER(UserInquiry) LIKE LOWER(:inquiry) LIMIT 1
                        """), {"inquiry": f"%{user_inquiry[:50]}%"})
                        saved_row = saved_result.fetchone()
                        
                        # Extract likely INI from inquiry (first 1-3 uppercase letters, case-insensitive)
                        import re
                        ini_matches = re.findall(r'\b[A-Za-z]{1,3}\b', user_inquiry.upper())
                        ini_guess = ini_matches[0] if ini_matches else None
                        
                        # Search SQL_SNIPPETS with best-guess INI and description (case-insensitive)
                        sql_rows = []
                        if ini_guess:
                            sql_result = conn.execute(text("""
                                SELECT Description, SQLCode, INI FROM SQL_SNIPPETS 
                                WHERE (UPPER(INI) = :ini OR LOWER(Description) LIKE LOWER(:inquiry)) 
                                LIMIT 2
                            """), {"ini": ini_guess.upper(), "inquiry": f"%{user_inquiry[:50]}%"})
                            sql_rows = sql_result.fetchall()
                        
                        # If no INI match, fall back to description only
                        if not sql_rows:
                            sql_result = conn.execute(text("""
                                SELECT Description, SQLCode, INI FROM SQL_SNIPPETS 
                                WHERE LOWER(Description) LIKE LOWER(:inquiry) 
                                LIMIT 2
                            """), {"inquiry": f"%{user_inquiry[:50]}%"})
                            sql_rows = sql_result.fetchall()
                        
                        # Search EPIC_LINKS with best-guess INI and description (case-insensitive)
                        links_rows = []
                        if ini_guess:
                            links_result = conn.execute(text("""
                                SELECT Description, URL, INI FROM EPIC_LINKS 
                                WHERE (UPPER(INI) = :ini OR LOWER(Description) LIKE LOWER(:inquiry))
                                LIMIT 2
                            """), {"ini": ini_guess.upper(), "inquiry": f"%{user_inquiry[:50]}%"})
                            links_rows = links_result.fetchall()
                        
                        # If no INI match, fall back to description only
                        if not links_rows:
                            links_result = conn.execute(text("""
                                SELECT Description, URL, INI FROM EPIC_LINKS 
                                WHERE LOWER(Description) LIKE LOWER(:inquiry)
                                LIMIT 2
                            """), {"inquiry": f"%{user_inquiry[:50]}%"})
                            links_rows = links_result.fetchall()
                        
                        # Build response from database matches
                        if saved_row or sql_rows or links_rows:
                            response_parts = []
                            
                            if saved_row:
                                response_parts.append(f"Previous Response: {saved_row[0][:200]}")
                            
                            if sql_rows:
                                response_parts.append("Related SQL Snippets:")
                                for row in sql_rows:
                                    desc, code = row[0], row[1]
                                    response_parts.append(f"  - {desc}: {code[:100]}")
                            
                            if links_rows:
                                response_parts.append("Related Documentation:")
                                for row in links_rows:
                                    desc, url = row[0], row[1]
                                    response_parts.append(f"  - {desc}: {url}")
                            
                            ai_response = "\n".join(response_parts)
                            response_source = "database_match"
                        else:
                            ai_response = "Hugging Face not configured and no related information found in database"
                            response_source = "no_match"
                except Exception as db_err:
                    print(f"[DB SEARCH ERROR] {db_err}")
                    ai_response = "Hugging Face not configured and database search failed"
                    response_source = "database_error"
            else:
                ai_response = "Hugging Face not configured and database unavailable"
                response_source = "no_service"
        
        # Save to database
        engine = get_db_engine()
        if engine:
            try:
                with engine.connect() as conn:
                    conn.execute(text("""
                        INSERT INTO SAVED_RESPONSES (UserInquiry, ResponseData, RequestDate, INI)
                        VALUES (:inquiry, :response, NOW(), :name)
                    """), {"inquiry": user_inquiry, "response": ai_response, "name": user_name})
                    conn.commit()
            except Exception as db_err:
                print(f"[DB INSERT ERROR] {db_err}")
        
        return {
            "status": "success",
            "user_name": user_name,
            "user_inquiry": user_inquiry,
            "ai_response": ai_response,
            "response_source": response_source,
            "has_pdf_context": bool(pdf_context),
            "message": "Inquiry processed successfully"
        }, 200
        
    except Exception as e:
        return {"error": f"Error: {str(e)}"}, 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
