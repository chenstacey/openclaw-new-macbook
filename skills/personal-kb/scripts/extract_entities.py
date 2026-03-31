#!/usr/bin/env python3
"""
Extract entities from text using simple NER patterns
"""

import sys
import json
import re

def extract_entities(text):
    """Extract entities from text using patterns"""
    entities = []
    
    # Company patterns
    company_patterns = [
        r'\b([A-Z][a-zA-Z]+ (?:Inc|Corp|Ltd|LLC|Company|Technologies|Systems|Group))\b',
        r'\b(Google|Apple|Microsoft|Amazon|Meta|Tesla|Twitter|X|OpenAI|Anthropic|Nvidia|Intel|AMD)\b'
    ]
    
    # Person patterns (simplified)
    person_patterns = [
        r'\b([A-Z][a-z]+ [A-Z][a-z]+)(?:,| is| was| said| announced)',
        r'(?:CEO|founder|president|director) ([A-Z][a-z]+ [A-Z][a-z]+)'
    ]
    
    # Technology/Concept patterns
    tech_patterns = [
        r'\b(Artificial Intelligence|AI|Machine Learning|ML|Blockchain|Cryptocurrency|Web3|Cloud Computing)\b',
        r'\b(Large Language Model|LLM|GPT|ChatGPT|Neural Network|Deep Learning)\b',
        r'\b(Startup|Venture Capital|IPO|Merger|Acquisition)\b'
    ]
    
    # Extract companies
    for pattern in company_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            entities.append({"name": match, "type": "Company"})
    
    # Extract people
    for pattern in person_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            if isinstance(match, tuple):
                match = match[0]
            entities.append({"name": match, "type": "Person"})
    
    # Extract concepts/technologies
    for pattern in tech_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            entities.append({"name": match, "type": "Concept"})
    
    # Deduplicate
    seen = set()
    unique_entities = []
    for e in entities:
        key = (e['name'].lower(), e['type'])
        if key not in seen:
            seen.add(key)
            unique_entities.append(e)
    
    return unique_entities

def main():
    if len(sys.argv) < 2:
        # Read from stdin
        text = sys.stdin.read()
    else:
        text = sys.argv[1]
    
    entities = extract_entities(text)
    print(json.dumps(entities, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()