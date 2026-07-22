#!/usr/bin/env python3
"""
Populate Missing Syllabus Topics & Chunks using Local Ollama LLM (gemma4:12b / qwen2:0.5b).
Injects vectorized chunks into chroma_db and ingestion_staging.db.
"""

import os
import sys
import json
import asyncio
import sqlite3
from pathlib import Path
from openai import AsyncOpenAI

# Set up paths
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from dotenv import load_dotenv
load_dotenv(BASE_DIR / ".env")

from core.syllabus_master import MASTER_SYLLABUS
import chromadb

OLLAMA_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434/v1")
MODEL_NAME = os.environ.get("OLLAMA_MODEL", "gemma4:12b")

client = AsyncOpenAI(api_key="ollama", base_url=OLLAMA_URL)

DB_DIR = BASE_DIR / "chroma_db"
chroma_client = chromadb.PersistentClient(path=str(DB_DIR))
collection = chroma_client.get_or_create_collection(name="exam_syllabus_collection")

STAGING_DB = BASE_DIR / "ingestion_staging.db"

def init_staging_db():
    conn = sqlite3.connect(str(STAGING_DB))
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS staging_chunks (
        id TEXT PRIMARY KEY,
        filename TEXT,
        subject TEXT,
        level TEXT,
        topic TEXT,
        content TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

async def generate_topic_chunk(subject: str, level: str, topic: str):
    prompt = f"""
You are an expert curriculum author for the National Curriculum Development Centre (NCDC) in Uganda.
Create a comprehensive teaching syllabus document chunk for:
Subject: {subject}
Class Level: {level}
Topic: {topic}

Requirements:
1. Include Learning Objectives (Competencies, Knowledge, Skills, Values).
2. Outline Subtopics, Key Terms, Definitions, and Formulas/Rules.
3. Provide 4 sample assessment questions with complete step-by-step solutions & marking guide.
4. Align with UNEB / NCDC standards for {level} in Uganda.

Format the output clearly as structured text.
"""
    try:
        response = await client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a professional educational curriculum designer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"  ❌ Error generating for {subject} - {level} - {topic}: {e}")
        return None

async def process_missing_topics(subject_filter=None, level_filter=None, max_topics=50):
    init_staging_db()
    print(f"🚀 Starting Ollama Syllabus Population using model: {MODEL_NAME}...")
    print(f"🔗 Ollama Endpoint: {OLLAMA_URL}")
    print(f"📦 ChromaDB Collection Count: {collection.count()}")

    conn = sqlite3.connect(str(STAGING_DB))
    cursor = conn.cursor()

    count = 0
    for subj, levels in MASTER_SYLLABUS.items():
        if subject_filter and subject_filter.lower() not in subj.lower():
            continue
            
        for lvl, topics in levels.items():
            if level_filter and level_filter.lower() not in lvl.lower():
                continue

            for t in topics:
                if count >= max_topics:
                    break

                # Check if chunk exists in ChromaDB
                doc_id = f"ollama_{subj}_{lvl}_{t}".replace(" ", "_").lower()
                existing = collection.get(ids=[doc_id])
                if existing and existing.get("ids"):
                    continue

                print(f"\n📖 Generating [{count+1}/{max_topics}] {subj} | {lvl} | Topic: '{t}'...")
                content = await generate_topic_chunk(subj, lvl, t)
                
                if not content:
                    continue

                # Add to ChromaDB
                collection.add(
                    ids=[doc_id],
                    documents=[content],
                    metadatas=[{
                        "subject": subj,
                        "level": lvl,
                        "topic": t,
                        "filename": f"Ollama_{MODEL_NAME}_Generated.txt",
                        "source": "ollama_local"
                    }]
                )

                # Add to Staging SQLite DB
                cursor.execute(
                    "INSERT OR REPLACE INTO staging_chunks (id, filename, subject, level, topic, content) VALUES (?, ?, ?, ?, ?, ?)",
                    (doc_id, f"Ollama_{MODEL_NAME}_Generated.txt", subj, lvl, t, content)
                )
                conn.commit()

                print(f"  ✓ Successfully vectorized & stored chunk: {doc_id}")
                count += 1

    conn.close()
    print(f"\n🎉 Population finished! Total new topics added: {count}")
    print(f"📊 Total Chunks now in ChromaDB: {collection.count()}")

if __name__ == "__main__":
    subj = sys.argv[1] if len(sys.argv) > 1 else None
    lvl = sys.argv[2] if len(sys.argv) > 2 else None
    max_t = int(sys.argv[3]) if len(sys.argv) > 3 else 20
    asyncio.run(process_missing_topics(subject_filter=subj, level_filter=lvl, max_topics=max_t))
