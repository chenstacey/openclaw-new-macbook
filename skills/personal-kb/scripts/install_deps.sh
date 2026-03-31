#!/bin/bash
# Install dependencies for Personal KB with Whisper

echo "🚀 Installing Personal KB Dependencies"
echo "======================================"
echo ""

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew not found. Please install it first:"
    echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    exit 1
fi

echo "📦 Installing packages..."

# Install yt-dlp
if ! command -v yt-dlp &> /dev/null; then
    echo "Installing yt-dlp..."
    brew install yt-dlp
else
    echo "✓ yt-dlp already installed"
fi

# Install ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "Installing ffmpeg..."
    brew install ffmpeg
else
    echo "✓ ffmpeg already installed"
fi

# Install Whisper
if ! command -v whisper &> /dev/null; then
    echo "Installing Whisper..."
    pip3 install openai-whisper
else
    echo "✓ Whisper already installed"
fi

echo ""
echo "✅ All dependencies installed!"
echo ""
echo "You can now process YouTube videos with:"
echo "  ~/.openclaw/workspace/skills/personal-kb/scripts/process_youtube.sh <youtube-url>"