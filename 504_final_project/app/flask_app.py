import pandas as pd
import flask
import requests
import time
import os
import json
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from huggingface_hub import InferenceClient
from PyPDF2 import PdfReader
from io import BytesIO

# Load environment variables
load_dotenv()

app = flask.Flask(__name__)

# Database configuration
sql_username = os.getenv("DB_APP_USERNAME")
sql_password = os.getenv("DB_APP_PASSWORD")
sql_hostname = os.getenv("DB_HOSTNAME")
sql_database = os.getenv("DB_DATABASE")
sql_port = os.getenv("DB_PORT", "3306")
hf_api_key = os.getenv("HUGGINGFACE_API_KEY")

# Initialize database engine (lazy connection - won't block startup)
engine = None
hf_client = None

def get_db_engine():
    """Initialize database connection lazily"""
    global engine
    if engine is None and all([sql_username, sql_password, sql_hostname, sql_database]):
        try:
            server_url = f"mysql+pymysql://{sql_username}:{sql_password}@{sql_hostname}:{sql_port}/{sql_database}"
            print("[STEP 1] Connecting to MySQL server:", server_url.replace(sql_password, "*****"))
            
            engine = create_engine(server_url, pool_pre_ping=True, connect_args={"ssl": {"ssl": True, "check_hostname": False, "ca": None}})
            
            # Test the connection
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                print("[STEP 2] Database connection successful!")
        except Exception as e:
            print(f"[ERROR] Database connection failed: {e}")
            engine = None
    return engine

def get_hf_client():
    """Initialize Hugging Face client lazily"""
    global hf_client
    if hf_client is None and hf_api_key:
        try:
            hf_client = InferenceClient(api_key=hf_api_key)
            print("[HF] Hugging Face client initialized")
        except Exception as e:
            print(f"[ERROR] Hugging Face initialization failed: {e}")
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
        print(f"[PDF] Error reading PDF: {e}")
    return ""

epicDataHandbookBaseURL = "https://datahandbook.epic.com/Search/Index?SearchWord=&type=6&sop=2&cin="

# Flask Routes
@app.route("/", methods=["GET"])
def home():
    return {"status": "Flask app is running on Cloud Run!", "message": "Hello from Cloud Run"}, 200

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for Cloud Run"""
    return {"status": "healthy"}, 200

@app.route("/api/data", methods=["GET"])
def get_data():
    """Fetch data from Cloud SQL"""
    db_engine = get_db_engine()
    if db_engine is None:
        return {"error": "Database not connected"}, 500
    
    try:
        with db_engine.connect() as conn:
            result = conn.execute(text("SELECT 1 as connection_test"))
            return {"status": "success", "data": "Connected to database"}, 200
    except Exception as e:
        return {"error": str(e)}, 500

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
            except Exception as e:
                ai_response = f"AI Error: {str(e)}"
        else:
            ai_response = "Hugging Face not configured"
        
        # Save to database
        db_engine = get_db_engine()
        if db_engine:
            try:
                with db_engine.connect() as conn:
                    conn.execute(text("""
                        INSERT INTO SAVED_RESPONSES (UserInquiry, ResponseData, RequestDate, INI)
                        VALUES (:inquiry, :response, NOW(), :name)
                    """), {"inquiry": user_inquiry, "response": ai_response, "name": user_name})
                    conn.commit()
                    print(f"[DB] Saved inquiry from {user_name}")
            except Exception as db_err:
                print(f"[DB] Insert error: {db_err}")
        
        return {
            "status": "success",
            "user_name": user_name,
            "user_inquiry": user_inquiry,
            "ai_response": ai_response,
            "has_pdf_context": bool(pdf_context),
            "message": "Inquiry processed successfully"
        }, 200
        
    except Exception as e:
        return {"error": f"Error: {str(e)}"}, 500

if __name__ == "__main__":
    # Listen on port 8080 for Cloud Run
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)