import os
import shutil

base = r"c:\Users\meher\OneDrive\Desktop\Personal Projects\Learning LangGraph\RAG"

folders_to_create = [
    "apps",
    "shared",
    "shared/config",
    "shared/ai_engine",
]

for fd in folders_to_create:
    os.makedirs(os.path.join(base, fd), exist_ok=True)

# 1. MOVE APPS
shutil.move(os.path.join(base, "fastapi_app"), os.path.join(base, "apps", "fastapi"))
shutil.move(os.path.join(base, "mcp_app"), os.path.join(base, "apps", "mcp"))
shutil.move(os.path.join(base, "frontend_app"), os.path.join(base, "apps", "frontend"))

# 2. MOVE SHARED LOGIC
shutil.move(os.path.join(base, "core", "config.py"), os.path.join(base, "shared", "config", "config.py"))
shutil.move(os.path.join(base, "core", "embeddings.py"), os.path.join(base, "shared", "ai_engine", "embeddings.py"))
shutil.move(os.path.join(base, "core", "ingestion.py"), os.path.join(base, "shared", "ai_engine", "ingestion.py"))
shutil.move(os.path.join(base, "db"), os.path.join(base, "shared", "db_layer"))
shutil.move(os.path.join(base, "graph"), os.path.join(base, "shared", "ai_engine", "graph"))
shutil.rmtree(os.path.join(base, "core"))  # clean up old core

# Create __init__.py files for imports to work
init_paths = [
    "shared/__init__.py",
    "shared/config/__init__.py",
    "shared/db_layer/__init__.py",
    "shared/ai_engine/__init__.py",
]
for p in init_paths:
    with open(os.path.join(base, p), 'w') as f:
        pass

# 3. FIX PYTHON IMPORTS GLOBALLY
replacements = [
    ("RAG.shared.config.config", "RAG.shared.config.config"),
    ("RAG.shared.ai_engine.embeddings", "RAG.shared.ai_engine.embeddings"),
    ("RAG.shared.ai_engine.ingestion", "RAG.shared.ai_engine.ingestion"),
    ("RAG.shared.db_layer", "RAG.shared.db_layer"),
    ("RAG.shared.ai_engine.graph", "RAG.shared.ai_engine.graph"),
    ("RAG.apps.fastapi", "RAG.apps.fastapi"),
    ("RAG.apps.mcp", "RAG.apps.mcp")
]

for root, dirs, files in os.walk(base):
    for name in files:
        if name.endswith(".py") or name == "Dockerfile":
            fpath = os.path.join(root, name)
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = content
            for old, new in replacements:
                new_content = new_content.replace(old, new)
                
            if new_content != content:
                with open(fpath, 'w', encoding='utf-8') as f:
                    f.write(new_content)

print("Migration Script Executed Successfully")
