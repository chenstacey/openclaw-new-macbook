#!/usr/bin/env python3
"""
Query personal knowledge base with semantic search
"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime, timedelta

OBSIDIAN_VAULT = Path.home() / "Documents" / "Obsidian Vault" / "Knowledge Base"
SOURCES_DIR = OBSIDIAN_VAULT / "Sources"
INDEX_FILE = OBSIDIAN_VAULT / "Index" / "source-index.json"

def load_index():
    """Load source index"""
    if INDEX_FILE.exists():
        return json.loads(INDEX_FILE.read_text())
    return []

def search_sources(query, index, time_weight=0.3, source_weight=1.0):
    """
    Search sources with ranking:
    - Semantic relevance (keyword matching as proxy)
    - Recency (time_weight)
    - Source type weighting
    """
    results = []
    query_lower = query.lower()
    query_terms = set(query_lower.split())
    
    for source in index:
        score = 0.0
        
        # Text relevance (simple keyword matching)
        title_lower = source.get('title', '').lower()
        entity_text = ' '.join(source.get('entities', [])).lower()
        
        title_matches = len(query_terms & set(title_lower.split()))
        entity_matches = len(query_terms & set(entity_text.split()))
        
        score += title_matches * 3.0  # Title matches weighted higher
        score += entity_matches * 2.0  # Entity matches weighted high
        
        # Recency boost
        try:
            ingested = datetime.fromisoformat(source['ingested'].replace('Z', '+00:00'))
            days_old = (datetime.now() - ingested).days
            recency_score = max(0, 1 - (days_old / 30))  # Decay over 30 days
            score += recency_score * time_weight * 10
        except:
            pass
        
        # Source type weighting
        source_type = source.get('type', 'article')
        type_weights = {
            'article': 1.0,
            'youtube': 0.9,
            'twitter': 0.8,
            'pdf': 1.1
        }
        score *= type_weights.get(source_type, 1.0) * source_weight
        
        if score > 0:
            results.append({
                **source,
                'relevance_score': round(score, 2)
            })
    
    # Sort by score
    results.sort(key=lambda x: x['relevance_score'], reverse=True)
    return results[:10]  # Top 10 results

def format_results(results, query):
    """Format search results for display"""
    if not results:
        return f"No sources found for: '{query}'"
    
    output = f"## Search Results: '{query}'\n\n"
    
    for i, result in enumerate(results, 1):
        output += f"### {i}. {result['title']}\n"
        output += f"- **Type:** {result['type']}\n"
        output += f"- **Relevance:** {result['relevance_score']}\n"
        output += f"- **URL:** {result['url']}\n"
        output += f"- **File:** [[{result['filepath']}|Open in Obsidian]]\n"
        
        if result.get('entities'):
            output += f"- **Entities:** {', '.join(result['entities'][:5])}\n"
        
        output += "\n"
    
    return output

def get_recent_sources(days=7, limit=10):
    """Get recently ingested sources"""
    index = load_index()
    cutoff = datetime.now() - timedelta(days=days)
    
    recent = []
    for source in index:
        try:
            ingested = datetime.fromisoformat(source['ingested'].replace('Z', '+00:00'))
            if ingested >= cutoff:
                recent.append(source)
        except:
            continue
    
    # Sort by date
    recent.sort(key=lambda x: x['ingested'], reverse=True)
    return recent[:limit]

def get_sources_by_entity(entity_name):
    """Get all sources mentioning an entity"""
    index = load_index()
    matches = []
    
    for source in index:
        entities = [e.lower() for e in source.get('entities', [])]
        if entity_name.lower() in entities:
            matches.append(source)
    
    return matches

def main():
    if len(sys.argv) < 2:
        print("Usage: query.py <query> [recent|entity]", file=sys.stderr)
        sys.exit(1)
    
    query = sys.argv[1]
    query_type = sys.argv[2] if len(sys.argv) > 2 else "search"
    
    index = load_index()
    
    if query_type == "recent":
        days = int(query) if query.isdigit() else 7
        results = get_recent_sources(days)
        output = f"## Recent Sources (Last {days} days)\n\n"
        for source in results:
            output += f"- **{source['title']}** ({source['type']}) - {source['ingested'][:10]}\n"
    
    elif query_type == "entity":
        results = get_sources_by_entity(query)
        output = f"## Sources about '{query}'\n\n"
        for source in results:
            output += f"- **{source['title']}** ({source['type']})\n"
    
    else:
        results = search_sources(query, index)
        output = format_results(results, query)
    
    print(output)

if __name__ == "__main__":
    main()