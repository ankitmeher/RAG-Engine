from RAG.shared.db_layer.connection import get_conn
import psycopg2.extras

def inspect_chunks():
    print("--- [CHUNK SCANNER] Reading actual text content... ---")
    try:
        with get_conn() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                # Get the latest session
                cur.execute("SELECT session_id FROM user_sessions ORDER BY created_at DESC LIMIT 1;")
                session = cur.fetchone()
                if not session:
                    print("❌ No sessions found.")
                    return
                
                s_id = session['session_id']
                print(f"Scanning Session: {s_id}")

                # Read all chunks for this session
                cur.execute("SELECT content_preview FROM document_chunks WHERE session_id = %s;", (s_id,))
                chunks = cur.fetchall()
                
                print(f"\nFound {len(chunks)} chunks:")
                for i, c in enumerate(chunks):
                    print(f"\n--- CHUNK {i+1} ---\n{c['content_preview']}\n------------------")

    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    inspect_chunks()
