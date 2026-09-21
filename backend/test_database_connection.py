"""Test database connection to diagnose 502 issue."""

from app.db.database import SessionLocal
from app.db.models.weather import WeatherRecord
from app.db.models.forecast import WeatherForecast


def test_database_connection():
    """Test if database connection works."""
    print("=" * 60)
    print("Testing Database Connection")
    print("=" * 60)
    
    try:
        db = SessionLocal()
        print("✓ Database session created")
        
        # Test a simple query
        records = db.query(WeatherRecord).limit(1).all()
        print(f"✓ Query successful, found {len(records)} records")
        
        db.close()
        print("✓ Database session closed")
        return True
    except Exception as e:
        print(f"✗ Database error: {type(e).__name__}: {e}")
        return False


if __name__ == "__main__":
    test_database_connection()
