# Mood Based Music App 🎵

A Python web application that suggests and plays music based on your current mood, with an intelligent LLM-powered feedback loop that learns and refines suggestions over time.

## Features

- 🎭 **Natural Language Mood Input**: Describe your mood in your own words (e.g., "feeling energetic after a workout", "melancholic and reflective")
- 🤖 **LLM-Powered Interpretation**: Uses Google Gemini (with Hugging Face fallback) to intelligently interpret your mood descriptions
- 🎬 **YouTube Integration**: Searches and embeds music videos directly in the app
- 🔄 **Per-Video Feedback Loop**: Rate each suggestion individually to help the app learn your preferences
- 💾 **Intelligent Learning**: Remembers your preferences and filters out disliked videos
- 🎨 **Beautiful Web Interface**: Modern, responsive design with embedded video players

## Demo

The app allows you to:
1. Describe your mood in natural language
2. Get intelligent music recommendations based on LLM interpretation
3. Watch videos directly in the app (no navigation away)
4. Provide feedback on each video (👍 Like, ⚪ Neutral, 👎 Dislike)
5. See improved suggestions over time as the app learns

## Setup

### Prerequisites

- Python 3.7 or higher
- YouTube Data API v3 key
- Google Gemini API key (optional but recommended for better interpretation)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/soumilsri/MoodBasedMusic.git
   cd MoodBasedMusic
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get API Keys:**
   - **YouTube API Key**: [Get it here](https://console.cloud.google.com/apis/credentials)
   - **Gemini API Key** (optional): [Get it here](https://makersuite.google.com/app/apikey)

4. **Configure environment:**
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` and add your API keys:
   ```
   YOUTUBE_API_KEY=your_youtube_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

5. **Run the application:**
   ```bash
   python app.py
   ```

6. **Open in browser:**
   - Navigate to: `http://localhost:5000`

## How It Works

### LLM-Powered Mood Interpretation

The app uses a smart fallback system:
1. **Primary**: Google Gemini (best quality, free tier)
2. **Fallback**: Hugging Face (if Gemini fails)
3. **Final Fallback**: Rule-based interpretation

### Learning System

- Tracks liked videos per mood
- Filters out disliked videos from future searches
- Remembers successful search queries
- Improves suggestions over time

### Feedback Loop

Each video has individual feedback buttons:
- 👍 **Like**: Saves the query and video for future use
- ⚪ **Neutral**: Records neutral feedback
- 👎 **Dislike**: Filters this video from future searches for this mood

## Project Structure

```
mood_music_app/
├── app.py                 # Main Flask application
├── mood_music_app.py      # CLI version (optional)
├── templates/
│   └── index.html         # Web interface
├── .env.example           # Environment template
├── .gitignore             # Git ignore rules
├── requirements.txt       # Python dependencies
├── SECURITY.md            # Security guidelines
├── check_secrets.py       # Pre-commit security check
└── README.md              # This file
```

## Security

⚠️ **IMPORTANT**: Never commit your `.env` file! It contains your private API keys.

- `.env` is automatically excluded via `.gitignore`
- Always use `.env.example` as a template
- Run `python check_secrets.py` before committing

See [SECURITY.md](SECURITY.md) for detailed security guidelines.

## API Keys

### YouTube Data API v3
- Free tier: 10,000 units per day (~100 searches)
- Get your key: https://console.cloud.google.com/apis/credentials

### Google Gemini API
- Free tier: 60 requests per minute
- Get your key: https://makersuite.google.com/app/apikey

## Technologies Used

- **Backend**: Python, Flask
- **LLM**: Google Gemini, Hugging Face
- **Frontend**: HTML, CSS, JavaScript
- **APIs**: YouTube Data API v3
- **Storage**: JSON (user preferences)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available for personal use.

## Author

Created as a POC for mood-based music recommendation with LLM integration.

## Acknowledgments

- YouTube Data API for music search
- Google Gemini for intelligent mood interpretation
- Hugging Face for free LLM fallback options

