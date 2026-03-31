#!/bin/bash
# Knowledge Base Ingestion Handler
# Called when URL is dropped in Telegram topic

WORKSPACE="/Users/openclaw/.openclaw/workspace"
SKILL_DIR="$WORKSPACE/skills/personal-kb"
URL="$1"

echo "🔍 Processing URL: $URL"

# Detect URL type
if [[ "$URL" == *"youtube.com"* ]] || [[ "$URL" == *"youtu.be"* ]]; then
    TYPE="youtube"
    echo "📺 Detected: YouTube video"
    
elif [[ "$URL" == *"twitter.com"* ]] || [[ "$URL" == *"x.com"* ]]; then
    TYPE="twitter"
    echo "🐦 Detected: Twitter/X thread"
    
elif [[ "$URL" == *.pdf ]]; then
    TYPE="pdf"
    echo "📄 Detected: PDF"
    
else
    TYPE="article"
    echo "📰 Detected: Web article"
fi

# The actual content extraction will be done by the agent
# This script just passes the URL to the processing pipeline
echo "{\"url\": \"$URL\", \"type\": \"$TYPE\", \"status\": \"pending\"}"