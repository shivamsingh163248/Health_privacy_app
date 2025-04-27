from models.database import get_connection

try:
    conn = get_connection()
    if conn.is_connected():
        print("✅ Database connection successful!")
    else:
        print("❌ Database connection failed!")
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    if 'conn' in locals() and conn.is_connected():
        conn.close()
