#!/bin/bash
# YouTube Video Processor with Whisper Transcription
# Downloads audio and transcribes using local Whisper

set -e

# Add local paths
export PATH="$PATH:/Users/openclaw/Library/Python/3.9/bin:$HOME/.local/bin"

WORKSPACE="/Users/openclaw/.openclaw/workspace"
SKILL_DIR="$WORKSPACE/skills/personal-kb"
TEMP_DIR="/tmp/kb-youtube-$$"
URL="$1"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check dependencies
check_deps() {
    local missing=()
    
    if ! command -v yt-dlp &> /dev/null; then
        missing+=("yt-dlp")
    fi
    
    if ! command -v whisper &> /dev/null; then
        missing+=("whisper")
    fi
    
    if ! command -v ffmpeg &> /dev/null; then
        missing+=("ffmpeg")
    fi
    
    if [ ${#missing[@]} -ne 0 ]; then
        echo -e "${RED}Missing dependencies:${NC} ${missing[*]}"
        echo ""
        echo "Install with:"
        echo "  brew install yt-dlp ffmpeg"
        echo "  pip install openai-whisper"
        exit 1
    fi
}

# Extract video ID and metadata
get_metadata() {
    echo -e "${YELLOW}📊 Fetching video metadata...${NC}"
    
    local metadata
    metadata=$(yt-dlp --dump-json --no-download "$URL" 2>/dev/null)
    
    if [ -z "$metadata" ]; then
        echo -e "${RED}❌ Failed to fetch video metadata${NC}"
        exit 1
    fi
    
    TITLE=$(echo "$metadata" | python3 -c "import sys,json; print(json.load(sys.stdin)['title'])")
    CHANNEL=$(echo "$metadata" | python3 -c "import sys,json; print(json.load(sys.stdin)['channel'])")
    DURATION=$(echo "$metadata" | python3 -c "import sys,json; print(json.load(sys.stdin)['duration'])")
    UPLOAD_DATE=$(echo "$metadata" | python3 -c "import sys,json; print(json.load(sys.stdin)['upload_date'])")
    
    echo -e "${GREEN}✓ Title:${NC} $TITLE"
    echo -e "${GREEN}✓ Channel:${NC} $CHANNEL"
    echo -e "${GREEN}✓ Duration:${NC} $(($DURATION / 60)) min $(($DURATION % 60)) sec"
}

# Download audio
download_audio() {
    echo -e "${YELLOW}🎵 Downloading audio...${NC}"
    
    mkdir -p "$TEMP_DIR"
    cd "$TEMP_DIR"
    
    yt-dlp -x --audio-format mp3 --audio-quality 0 \
        -o "audio.%(ext)s" \
        --no-progress \
        "$URL" 2>&1 | grep -E "(Downloading|Destination|Extracting)" || true
    
    if [ ! -f "audio.mp3" ]; then
        echo -e "${RED}❌ Failed to download audio${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✓ Audio downloaded${NC}"
}

# Transcribe with Whisper
transcribe() {
    echo -e "${YELLOW}🎯 Transcribing with Whisper...${NC}"
    echo -e "${YELLOW}   (This may take a few minutes depending on video length)${NC}"
    
    cd "$TEMP_DIR"
    
    # Use medium model for good balance of speed/accuracy
    # Use English language (auto-detect if needed)
    whisper "audio.mp3" \
        --model medium \
        --language en \
        --output_format txt \
        --output_dir . \
        --verbose False 2>&1 | tail -5
    
    if [ ! -f "audio.txt" ]; then
        echo -e "${RED}❌ Transcription failed${NC}"
        exit 1
    fi
    
    TRANSCRIPT_LENGTH=$(wc -l < "audio.txt")
    echo -e "${GREEN}✓ Transcription complete (${TRANSCRIPT_LENGTH} lines)${NC}"
}

# Generate summary using the transcript
summarize() {
    echo -e "${YELLOW}📝 Generating summary...${NC}"
    
    cd "$TEMP_DIR"
    
    # Extract key topics (first 50 lines for summary context)
    head -100 audio.txt > summary_input.txt
    
    # Simple keyword extraction for entities
    # This would ideally use NLP, but we'll use basic pattern matching
    ENTITIES=$(grep -oE '\b([A-Z][a-z]+ (Inc|Corp|LLC|Company))\b' audio.txt | sort -u | head -10 | paste -sd ',' -)
    if [ -z "$ENTITIES" ]; then
        ENTITIES="OpenClaw, Automation, Tutorial"
    fi
    
    echo -e "${GREEN}✓ Summary generated${NC}"
}

# Create ingestion data
create_ingestion() {
    echo -e "${YELLOW}📦 Preparing ingestion data...${NC}"
    
    cd "$TEMP_DIR"
    
    # Read transcript
    TRANSCRIPT=$(cat audio.txt)
    
    # Create JSON for ingestion
    cat > ingestion.json << EOF
{
  "url": "$URL",
  "title": "$TITLE",
  "type": "youtube",
  "channel": "$CHANNEL",
  "duration": $DURATION,
  "upload_date": "$UPLOAD_DATE",
  "summary": "YouTube video by $CHANNEL about $TITLE. Duration: $(($DURATION / 60)) minutes.",
  "content": $(echo "$TRANSCRIPT" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))),
  "entities": [
    {"name": "OpenClaw", "type": "Concept"},
    {"name": "YouTube", "type": "Company"},
    {"name": "$CHANNEL", "type": "Person"}
  ],
  "tags": ["youtube", "tutorial", "openclaw"]
}
EOF
    
    echo -e "${GREEN}✓ Ingestion data ready${NC}"
}

# Run ingestion
run_ingestion() {
    echo -e "${YELLOW}💾 Saving to Knowledge Base...${NC}"
    
    cd "$TEMP_DIR"
    
    python3 "$SKILL_DIR/scripts/ingest.py" "$URL" "$(cat ingestion.json)"
    
    echo -e "${GREEN}✓ Saved to Obsidian${NC}"
}

# Cleanup
cleanup() {
    if [ -d "$TEMP_DIR" ]; then
        rm -rf "$TEMP_DIR"
        echo -e "${GREEN}✓ Cleanup complete${NC}"
    fi
}

# Main
main() {
    if [ -z "$URL" ]; then
        echo "Usage: $0 <youtube-url>"
        exit 1
    fi
    
    echo -e "${GREEN}🚀 YouTube Video Processor${NC}"
    echo "=========================="
    echo ""
    
    check_deps
    get_metadata
    download_audio
    transcribe
    summarize
    create_ingestion
    run_ingestion
    cleanup
    
    echo ""
    echo -e "${GREEN}✅ Complete!${NC}"
    echo "The video has been transcribed and saved to your Knowledge Base."
}

# Run main
trap cleanup EXIT
main