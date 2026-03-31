#!/usr/bin/env python3
"""
Personal Knowledge Base Ingester
Processes URLs from Telegram and saves to Obsidian
"""

import sys
import json
import re
import hashlib
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse, parse_qs

# Configuration
OBSIDIAN_VAULT = Path.home() / "Documents" / "Obsidian Vault" / "Knowledge Base"
SOURCES_DIR = OBSIDIAN_VAULT / "Sources"
ENTITIES_DIR = OBSIDIAN_VAULT / "Entities"
INDEX_FILE = OBSIDIAN_VAULT / "Index" / "source-index.json"

def ensure_dirs():
    """Create necessary directories"""
    SOURCES_DIR.mkdir(parents=True, exist_ok=True)
    (ENTITIES_DIR / "People").mkdir(parents=True, exist_ok=True)
    (ENTITIES_DIR / "Companies").mkdir(parents=True, exist_ok=True)
    (ENTITIES_DIR / "Concepts").mkdir(parents=True, exist_ok=True)
    (ENTITIES_DIR / "Locations").mkdir(parents=True, exist_ok=True)
    (OBSIDIAN_VAULT / "Index").mkdir(parents=True, exist_ok=True)

def detect_url_type(url):
    """Detect the type of URL"""
    url_lower = url.lower()
    
    if "youtube.com" in url_lower or "youtu.be" in url_lower:
        return "youtube"
    elif "twitter.com" in url_lower or "x.com" in url_lower:
        return "twitter"
    elif url_lower.endswith(".pdf"):
        return "pdf"
    else:
        return "article"

def extract_youtube_id(url):
    """Extract YouTube video ID"""
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})',
        r'youtube\.com/shorts/([a-zA-Z0-9_-]{11})'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def extract_twitter_id(url):
    """Extract Twitter/X tweet ID"""
    pattern = r'(?:twitter\.com|x\.com)/\w+/status/(\d+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

def sanitize_filename(title):
    """Create safe filename from title"""
    # Remove special characters
    safe = re.sub(r'[^\w\s-]', '', title)
    safe = re.sub(r'[-\s]+', '-', safe)
    return safe[:100].strip('-')

def create_source_file(ingestion_data):
    """Create Obsidian markdown file for source"""
    date_str = datetime.now().strftime("%Y-%m-%d")
    safe_title = sanitize_filename(ingestion_data['title'])
    filename = f"{date_str}-{safe_title}.md"
    filepath = SOURCES_DIR / filename
    
    # Build frontmatter
    frontmatter = {
        "title": ingestion_data['title'],
        "url": ingestion_data['url'],
        "ingested": datetime.now().isoformat(),
        "source_type": ingestion_data['type'],
        "entities": ingestion_data.get('entities', []),
        "tags": ingestion_data.get('tags', [])
    }
    
    # Build content
    content = f"""---
{json.dumps(frontmatter, indent=2, ensure_ascii=False)}
---

# {ingestion_data['title']}

**Source:** [{ingestion_data['url']}]({ingestion_data['url']})  
**Type:** {ingestion_data['type']}  
**Ingested:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

## Summary

{ingestion_data.get('summary', 'No summary available.')}

## Content

{ingestion_data.get('content', 'Content extraction failed.')}

## Entities

"""
    
    # Add entity links
    for entity in ingestion_data.get('entities', []):
        entity_type = entity.get('type', 'Concept')
        entity_name = entity.get('name', 'Unknown')
        content += f"- [[{entity_name}]] ({entity_type})\n"
    
    # Write file
    filepath.write_text(content, encoding='utf-8')
    return filepath

def update_index(ingestion_data, filepath):
    """Update source index"""
    INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    index = []
    if INDEX_FILE.exists():
        index = json.loads(INDEX_FILE.read_text())
    
    index.append({
        "id": hashlib.md5(ingestion_data['url'].encode()).hexdigest()[:8],
        "title": ingestion_data['title'],
        "url": ingestion_data['url'],
        "type": ingestion_data['type'],
        "filepath": str(filepath.relative_to(OBSIDIAN_VAULT)),
        "ingested": datetime.now().isoformat(),
        "entities": [e['name'] for e in ingestion_data.get('entities', [])]
    })
    
    INDEX_FILE.write_text(json.dumps(index, indent=2, ensure_ascii=False))

def create_entity_files(entities):
    """Create/update entity files"""
    for entity in entities:
        name = entity['name']
        entity_type = entity.get('type', 'Concept')
        
        # Determine folder
        if entity_type == 'Person':
            folder = ENTITIES_DIR / "People"
        elif entity_type == 'Company':
            folder = ENTITIES_DIR / "Companies"
        elif entity_type == 'Location':
            folder = ENTITIES_DIR / "Locations"
        else:
            folder = ENTITIES_DIR / "Concepts"
        
        filepath = folder / f"{name}.md"
        
        if not filepath.exists():
            content = f"""# {name}

**Type:** {entity_type}

## Sources

"""
            filepath.write_text(content, encoding='utf-8')

def main():
    if len(sys.argv) < 2:
        print("Usage: ingest.py <url> [content_json]", file=sys.stderr)
        sys.exit(1)
    
    url = sys.argv[1]
    content_data = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    
    ensure_dirs()
    
    # Detect URL type
    url_type = detect_url_type(url)
    
    # Prepare ingestion data
    ingestion_data = {
        'url': url,
        'type': url_type,
        'title': content_data.get('title', 'Untitled'),
        'summary': content_data.get('summary', ''),
        'content': content_data.get('content', ''),
        'entities': content_data.get('entities', []),
        'tags': content_data.get('tags', [])
    }
    
    # Create source file
    filepath = create_source_file(ingestion_data)
    
    # Update index
    update_index(ingestion_data, filepath)
    
    # Create entity files
    create_entity_files(ingestion_data['entities'])
    
    print(json.dumps({
        "success": True,
        "filepath": str(filepath),
        "type": url_type,
        "entities": len(ingestion_data['entities'])
    }))

if __name__ == "__main__":
    main()