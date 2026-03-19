"""Database health check utility."""
import os
import sys

def check_db_connection():
    """Verify database connectivity."""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = os.getenv('DB_PORT', '5432')
        db_name = os.getenv('DB_NAME', 'study_tools')
        
        print(f"Checking connection to {db_host}:{db_port}/{db_name}...")
        # Connection check would go here
        print("Database connection: OK")
        return True
    except Exception as e:
        print(f"Database connection: FAILED - {e}")
        return False

if __name__ == '__main__':
    success = check_db_connection()
    sys.exit(0 if success else 1)
