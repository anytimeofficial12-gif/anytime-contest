"""
FastAPI Backend for ANYTIME Contest
Stores contestant data in Google Sheets
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, validator
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
from datetime import datetime
from typing import Optional
import logging

# Environment configuration
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
DEBUG_MODE = ENVIRONMENT == 'development'

# Configure logging based on environment
log_level = logging.DEBUG if DEBUG_MODE else logging.INFO
logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log') if not DEBUG_MODE else logging.NullHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="ANYTIME Contest API",
    description="Backend API for storing contest submissions in Google Sheets",
    version="1.0.0"
)

# CORS middleware for frontend integration
# Configure CORS for production deployment
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
]

# In Vercel, frontend and backend share the same origin. Allow all origins in production
# or dynamically allow the request origin. Here we enable all in production to simplify.
allow_all_origins = os.getenv("ALLOW_ALL_ORIGINS", "true").lower() == "true"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if allow_all_origins else ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class ContestSubmission(BaseModel):
    name: str
    email: str
    answer: str
    timestamp: Optional[str] = None
    
    @validator('name')
    def validate_name(cls, v):
        if not v or len(v.strip()) < 2:
            raise ValueError('Name must be at least 2 characters long')
        return v.strip()
    
    @validator('email')
    def validate_email(cls, v):
        if not v or '@' not in v:
            raise ValueError('Valid email address required')
        return v.strip().lower()
    
    @validator('answer')
    def validate_answer(cls, v):
        if not v or len(v.strip()) < 5:
            raise ValueError('Answer must be at least 5 characters long')
        return v.strip()

class SubmissionResponse(BaseModel):
    success: bool
    message: str
    submission_id: Optional[str] = None

# Google Sheets configuration
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = os.getenv('GOOGLE_SERVICE_ACCOUNT_FILE', 'contestdata-472704-c4b8568d4dcb.json')
SPREADSHEET_ID = os.getenv('GOOGLE_SPREADSHEET_ID', '1tKrJieYsoHpFJzi1bZ5Z28XSzxidikVTXmoyvWxw2VQ')
RANGE_NAME = os.getenv('GOOGLE_SHEET_RANGE', 'Sheet1!A:D')

# Global variable for Google Sheets service
sheets_service = None

def initialize_google_sheets():
    """Initialize Google Sheets API service"""
    global sheets_service
    try:
        # Try to get credentials from environment variable first (for production)
        google_credentials_json = os.getenv('GOOGLE_CREDENTIALS_JSON')
        
        if google_credentials_json:
            # Use credentials from environment variable
            import json
            credentials_info = json.loads(google_credentials_json)
            credentials = service_account.Credentials.from_service_account_info(
                credentials_info, scopes=SCOPES
            )
            logger.info("Google Sheets API initialized from environment credentials")
        elif os.path.exists(SERVICE_ACCOUNT_FILE):
            # Use credentials from file (for local development)
            credentials = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES
            )
            logger.info("Google Sheets API initialized from service account file")
        else:
            raise FileNotFoundError(f"Service account file {SERVICE_ACCOUNT_FILE} not found and no environment credentials provided")
        
        sheets_service = build('sheets', 'v4', credentials=credentials)
        logger.info("Google Sheets API initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize Google Sheets API: {str(e)}")
        return False

def append_to_sheet(data: ContestSubmission) -> bool:
    """Append contest submission to Google Sheet"""
    try:
        if not sheets_service:
            logger.warning("Google Sheets service not initialized, using fallback storage")
            return append_to_local_storage(data)
        
        # Prepare the row data
        timestamp = data.timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        values = [[data.name, data.email, data.answer, timestamp]]
        
        # Append to sheet
        body = {'values': values}
        result = sheets_service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body=body
        ).execute()
        
        logger.info(f"Successfully appended data to sheet: {result.get('updates', {}).get('updatedRows', 0)} rows updated")
        return True
        
    except HttpError as e:
        logger.error(f"Google Sheets API error: {str(e)}")
        logger.info("Falling back to local storage")
        return append_to_local_storage(data)
    except Exception as e:
        logger.error(f"Error appending to sheet: {str(e)}")
        logger.info("Falling back to local storage")
        return append_to_local_storage(data)

def append_to_local_storage(data: ContestSubmission) -> bool:
    """Fallback: Append contest submission to local JSON file"""
    try:
        import json
        
        # Load existing submissions
        submissions_file = 'contest_submissions_backup.json'
        try:
            with open(submissions_file, 'r', encoding='utf-8') as f:
                submissions = json.load(f)
        except FileNotFoundError:
            submissions = []
        
        # Add new submission
        timestamp = data.timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        submission = {
            "id": f"sub_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "name": data.name,
            "email": data.email,
            "answer": data.answer,
            "timestamp": timestamp,
            "submitted_at": datetime.now().isoformat(),
            "storage_method": "local_backup"
        }
        
        submissions.append(submission)
        
        # Save back to file
        with open(submissions_file, 'w', encoding='utf-8') as f:
            json.dump(submissions, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Successfully saved submission to local backup: {submission['id']}")
        return True
        
    except Exception as e:
        logger.error(f"Error saving to local storage: {str(e)}")
        return False

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info(f"Starting ANYTIME Contest API in {ENVIRONMENT} mode")
    logger.info(f"Allowed CORS origins: {ALLOWED_ORIGINS}")
    
    if not initialize_google_sheets():
        logger.warning("Failed to initialize Google Sheets. Will use local storage fallback.")
        if DEBUG_MODE:
            logger.info("To fix Google Sheets: Share your sheet with contestdataa@contestdata-472704.iam.gserviceaccount.com")
    else:
        logger.info("Google Sheets integration ready")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "ANYTIME Contest API is running",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    sheets_status = "connected" if sheets_service else "disconnected"
    return {
        "status": "healthy",
        "environment": ENVIRONMENT,
        "google_sheets": sheets_status,
        "cors_origins": ALLOWED_ORIGINS,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/submit", response_model=SubmissionResponse)
async def submit_contest_entry(submission: ContestSubmission):
    """
    Submit a contest entry and store it in Google Sheets
    """
    try:
        # Validate that Google Sheets is available
        if not sheets_service:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Google Sheets service is not available"
            )
        
        # Add timestamp if not provided
        if not submission.timestamp:
            submission.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Append to Google Sheet
        success = append_to_sheet(submission)
        
        if success:
            logger.info(f"Successfully stored submission for {submission.email}")
            return SubmissionResponse(
                success=True,
                message="Submission recorded successfully!",
                submission_id=f"sub_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to store submission. Please try again."
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in submit_contest_entry: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again later."
        )

@app.get("/submissions/count")
async def get_submission_count():
    """Get the total number of submissions (optional endpoint)"""
    try:
        # Try Google Sheets first
        if sheets_service:
            try:
                result = sheets_service.spreadsheets().values().get(
                    spreadsheetId=SPREADSHEET_ID,
                    range=RANGE_NAME
                ).execute()
                
                values = result.get('values', [])
                # Subtract 1 for header row
                count = max(0, len(values) - 1) if values else 0
                
                return {
                    "total_submissions": count,
                    "storage_method": "google_sheets",
                    "timestamp": datetime.now().isoformat()
                }
            except Exception as e:
                logger.warning(f"Google Sheets count failed: {e}, trying local backup")
        
        # Fallback to local storage
        try:
            import json
            with open('contest_submissions_backup.json', 'r', encoding='utf-8') as f:
                submissions = json.load(f)
            
            return {
                "total_submissions": len(submissions),
                "storage_method": "local_backup",
                "timestamp": datetime.now().isoformat()
            }
        except FileNotFoundError:
            return {
                "total_submissions": 0,
                "storage_method": "none",
                "timestamp": datetime.now().isoformat()
            }
        
    except Exception as e:
        logger.error(f"Error getting submission count: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve submission count"
        )

@app.get("/submissions/backup")
async def get_backup_submissions():
    """Get submissions from local backup file or Google Sheets"""
    try:
        # Try Google Sheets first
        if sheets_service:
            try:
                result = sheets_service.spreadsheets().values().get(
                    spreadsheetId=SPREADSHEET_ID,
                    range=RANGE_NAME
                ).execute()
                
                values = result.get('values', [])
                submissions = []
                
                # Skip header row and convert to submission format
                for i, row in enumerate(values[1:], 1):
                    if len(row) >= 4:  # Ensure we have all required fields
                        submission = {
                            "id": f"sub_gs_{i}",
                            "name": row[0] if len(row) > 0 else "",
                            "email": row[1] if len(row) > 1 else "",
                            "answer": row[2] if len(row) > 2 else "",
                            "timestamp": row[3] if len(row) > 3 else "",
                            "submitted_at": row[3] if len(row) > 3 else "",
                            "storage_method": "google_sheets"
                        }
                        submissions.append(submission)
                
                return {
                    "total_submissions": len(submissions),
                    "submissions": submissions,
                    "storage_method": "google_sheets",
                    "timestamp": datetime.now().isoformat()
                }
            except Exception as e:
                logger.warning(f"Google Sheets read failed: {e}, trying local backup")
        
        # Fallback to local backup
        import json
        with open('contest_submissions_backup.json', 'r', encoding='utf-8') as f:
            submissions = json.load(f)
        
        return {
            "total_submissions": len(submissions),
            "submissions": submissions,
            "storage_method": "local_backup",
            "timestamp": datetime.now().isoformat()
        }
    except FileNotFoundError:
        return {
            "total_submissions": 0,
            "submissions": [],
            "storage_method": "none",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting submissions: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve submissions"
        )

@app.get("/submissions/sync")
async def sync_google_sheets():
    """Force sync data from Google Sheets and return fresh data"""
    try:
        if not sheets_service:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Google Sheets service is not available"
            )
        
        # Force read from Google Sheets
        result = sheets_service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME
        ).execute()
        
        values = result.get('values', [])
        submissions = []
        
        # Skip header row and convert to submission format
        for i, row in enumerate(values[1:], 1):
            if len(row) >= 4:  # Ensure we have all required fields
                submission = {
                    "id": f"sub_gs_{i}",
                    "name": row[0] if len(row) > 0 else "",
                    "email": row[1] if len(row) > 1 else "",
                    "answer": row[2] if len(row) > 2 else "",
                    "timestamp": row[3] if len(row) > 3 else "",
                    "submitted_at": row[3] if len(row) > 3 else "",
                    "storage_method": "google_sheets",
                    "synced_at": datetime.now().isoformat()
                }
                submissions.append(submission)
        
        # Also save to local backup for offline access
        try:
            import json
            backup_data = {
                "total_submissions": len(submissions),
                "submissions": submissions,
                "last_sync": datetime.now().isoformat(),
                "source": "google_sheets_sync"
            }
            with open('contest_submissions_synced.json', 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.warning(f"Failed to save local backup: {e}")
        
        return {
            "total_submissions": len(submissions),
            "submissions": submissions,
            "storage_method": "google_sheets",
            "sync_status": "success",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error syncing Google Sheets: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to sync Google Sheets: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment variable (for deployment platforms)
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    # Configure uvicorn based on environment
    if DEBUG_MODE:
        uvicorn.run(
            "app:app", 
            host=host, 
            port=port, 
            reload=True,
            log_level="debug"
        )
    else:
        uvicorn.run(
            "app:app", 
            host=host, 
            port=port, 
            workers=1,
            log_level="info"
        )
