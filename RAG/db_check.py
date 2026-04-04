from RAG.shared.db_layer.connection import get_conn
import psycopg2.extras

def check_db():
    print("--- [DATABASE EXPLORER] Identifying active sessions... ---")
    try:
        with get_conn() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                # 1. Check user sessions
                cur.execute("SELECT session_id, created_at FROM user_sessions ORDER BY created_at DESC LIMIT 5;")
                sessions = cur.fetchall()
                print(f"Found {len(sessions)} recent sessions:")
                for s in sessions:
                    print(f" - {s['session_id']} (Created: {s['created_at']})")
                
                if not sessions:
                    print("⚠️ No sessions found in user_sessions table!")
                    return

                # 2. Check chunks for the latest session
                latest_id = sessions[0]['session_id']
                cur.execute("SELECT COUNT(*) FROM document_chunks WHERE session_id = %s;", (latest_id,))
                count = cur.fetchone()['count']
                print(f"\n✅ LATEST ID: {latest_id}")
                print(f"📊 CHUNK COUNT: {count}")
                
                if count > 0:
                    print("\n🎉 YOUR DATA IS READY! You can now use the browser!")
                else:
                    print("\n⚠️ This session has 0 chunks. Try uploading your PDF again in the UI.")

    except Exception as e:
        print(f"❌ DATABASE ERROR: {e}")

if __name__ == "__main__":
    check_db()
