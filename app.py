#!/usr/bin/env python3
"""
Mood Music App - Web Version
Flask web application for mood-based music discovery
"""

import os
import json
import random
import requests
from typing import Dict, List, Optional
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

class MoodMusicApp:
    def __init__(self):
        self.api_key = os.getenv('YOUTUBE_API_KEY')
        # Free LLM options
        self.huggingface_key = os.getenv('HUGGINGFACE_API_KEY')
        self.gemini_key = os.getenv('GEMINI_API_KEY')
        self.llm_provider = os.getenv('LLM_PROVIDER', 'huggingface').lower()  # huggingface, gemini, or none
        self.preferences_file = 'user_preferences.json'
        self.preferences = self.load_preferences()
        
    def load_preferences(self) -> Dict:
        """Load user preferences from file"""
        if os.path.exists(self.preferences_file):
            try:
                with open(self.preferences_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {
            'mood_history': [],
            'feedback_history': [],
            'refined_keywords': {}
        }
    
    def save_preferences(self):
        """Save user preferences to file"""
        with open(self.preferences_file, 'w') as f:
            json.dump(self.preferences, f, indent=2)
    
    def refine_keywords(self, mood_description: str, feedback: str, query: str, video_id: str = None, video_title: str = None):
        """Refine keywords based on user feedback"""
        mood_normalized = mood_description.lower().strip()
        
        if mood_normalized not in self.preferences['refined_keywords']:
            self.preferences['refined_keywords'][mood_normalized] = {
                'liked_keywords': [],
                'disliked_keywords': [],
                'successful_queries': [],
                'liked_videos': [],
                'disliked_videos': []
            }
        
        # Store detailed feedback for learning
        feedback_entry = {
            'mood': mood_description,
            'mood_normalized': mood_normalized,
            'feedback': feedback,
            'query': query,
            'video_id': video_id,
            'video_title': video_title,
            'timestamp': datetime.now().isoformat()
        }
        self.preferences['feedback_history'].append(feedback_entry)
        
        # Learn from feedback
        if feedback == 'like':
            if query not in self.preferences['refined_keywords'][mood_normalized]['successful_queries']:
                self.preferences['refined_keywords'][mood_normalized]['successful_queries'].append(query)
            if video_id and video_id not in self.preferences['refined_keywords'][mood_normalized]['liked_videos']:
                self.preferences['refined_keywords'][mood_normalized]['liked_videos'].append({
                    'video_id': video_id,
                    'title': video_title,
                    'timestamp': datetime.now().isoformat()
                })
        elif feedback == 'dislike':
            if video_id and video_id not in self.preferences['refined_keywords'][mood_normalized]['disliked_videos']:
                self.preferences['refined_keywords'][mood_normalized]['disliked_videos'].append({
                    'video_id': video_id,
                    'title': video_title,
                    'timestamp': datetime.now().isoformat()
                })
    
    def interpret_mood_with_llm(self, mood_description: str) -> Dict[str, str]:
        """Use free LLM to interpret the mood description and generate search query"""
        # Default: Try Gemini first (best quality), then fallback to Hugging Face
        
        # Try Google Gemini first (if API key is available)
        if self.gemini_key:
            try:
                return self._interpret_with_gemini(mood_description)
            except Exception as e:
                print(f"Gemini failed, falling back to Hugging Face: {e}")
                # Continue to Hugging Face fallback below
        
        # Fallback to Hugging Face (with API key if available)
        if self.huggingface_key:
            try:
                return self._interpret_with_huggingface(mood_description)
            except Exception as e:
                print(f"Hugging Face API failed, using public method: {e}")
                # Continue to public method below
        
        # Fallback to Hugging Face public (no API key needed)
        try:
            return self._interpret_with_huggingface_public(mood_description)
        except Exception as e:
            print(f"All LLM methods failed: {e}")
        
        # Final fallback: simple keyword extraction
        return {
            'mood_label': mood_description.lower(),
            'search_query': f"{mood_description} music",
            'interpretation': mood_description
        }
    
    def _interpret_with_huggingface(self, mood_description: str) -> Dict[str, str]:
        """Use Hugging Face Inference API (free tier)"""
        try:
            prompt = f"""You are a music recommendation assistant. A user described their mood as: "{mood_description}"

Based on this description, generate:
1. A concise mood label (1-2 words)
2. An optimized YouTube music search query (3-5 words)
3. A brief interpretation

Respond in JSON format:
{{"mood_label": "...", "search_query": "...", "interpretation": "..."}}"""

            headers = {
                "Authorization": f"Bearer {self.huggingface_key}",
                "Content-Type": "application/json"
            }
            
            # Using a free model like mistralai/Mistral-7B-Instruct-v0.2 or meta-llama/Llama-2-7b-chat-hf
            # For free tier, we'll use a simpler approach with a text generation model
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 150,
                    "temperature": 0.7,
                    "return_full_text": False
                }
            }
            
            # Try using a free model endpoint
            response = requests.post(
                "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result_text = response.json()[0].get('generated_text', '').strip()
                # Try to extract JSON from response
                import re
                json_match = re.search(r'\{[^}]+\}', result_text)
                if json_match:
                    result = json.loads(json_match.group())
                    return result
        except Exception as e:
            print(f"Hugging Face API error: {e}")
            # Raise exception so caller can handle fallback
            raise
    
    def _interpret_with_huggingface_public(self, mood_description: str) -> Dict[str, str]:
        """Use Hugging Face public models (no API key needed, but slower)"""
        try:
            # Improved rule-based interpretation that handles negations
            mood_lower = mood_description.lower()
            
            # Check for negations first (not, nor, neither, etc.)
            negation_words = ['not', 'nor', 'neither', "don't", "doesn't", "isn't", "aren't", "won't", "can't"]
            has_negation = any(neg in mood_lower for neg in negation_words)
            
            # Extract key emotions/words
            mood_keywords = {
                'happy': ['happy', 'joyful', 'cheerful', 'upbeat', 'excited', 'celebrating', 'glad', 'pleased'],
                'sad': ['sad', 'down', 'depressed', 'melancholic', 'lonely', 'heartbroken', 'breakup', 'upset', 'unhappy'],
                'energetic': ['energetic', 'pumped', 'workout', 'exercise', 'active', 'motivated', 'pumped up'],
                'relaxed': ['relaxed', 'chill', 'calm', 'peaceful', 'meditation', 'zen', 'serene', 'tranquil'],
                'focused': ['focused', 'study', 'work', 'concentration', 'productive', 'lo-fi', 'studying', 'working'],
                'romantic': ['romantic', 'love', 'intimate', 'dating', 'relationship', 'loving'],
                'angry': ['angry', 'frustrated', 'aggressive', 'intense', 'heavy', 'mad', 'irritated'],
                'nostalgic': ['nostalgic', 'retro', 'vintage', 'old', 'classic', 'memories', 'remembering'],
                'neutral': ['neutral', 'indifferent', 'neither', 'ambivalent', 'mixed', 'confused']
            }
            
            detected_mood = 'neutral'
            mood_scores = {}
            
            # Score each mood based on keyword matches
            for mood, keywords in mood_keywords.items():
                score = 0
                for keyword in keywords:
                    if keyword in mood_lower:
                        # If there's a negation before the keyword, subtract points
                        keyword_index = mood_lower.find(keyword)
                        if keyword_index > 0:
                            # Check for negation words before the keyword (within 10 chars)
                            context = mood_lower[max(0, keyword_index-15):keyword_index]
                            if any(neg in context for neg in negation_words):
                                score -= 2  # Strong negative signal
                            else:
                                score += 1
                        else:
                            score += 1
                mood_scores[mood] = score
            
            # Find the mood with highest positive score
            max_score = max(mood_scores.values())
            if max_score > 0:
                detected_mood = max(mood_scores, key=mood_scores.get)
            else:
                # If all scores are negative or zero, it's truly neutral/ambiguous
                detected_mood = 'neutral'
            
            # Generate search query based on detected mood
            if detected_mood == 'happy':
                search_query = "upbeat happy energetic music"
            elif detected_mood == 'sad':
                search_query = "sad emotional melancholic music"
            elif detected_mood == 'energetic':
                search_query = "high energy motivational music"
            elif detected_mood == 'relaxed':
                search_query = "chill ambient peaceful music"
            elif detected_mood == 'focused':
                search_query = "study focus instrumental music"
            elif detected_mood == 'romantic':
                search_query = "romantic love songs music"
            elif detected_mood == 'angry':
                search_query = "intense powerful aggressive music"
            elif detected_mood == 'nostalgic':
                search_query = "classic retro vintage music"
            elif detected_mood == 'neutral':
                # For neutral/ambiguous moods, use ambient or instrumental
                search_query = "ambient instrumental background music"
            else:
                # Extract key words from description, avoiding negations
                words = mood_lower.split()
                # Remove common words and negations
                stop_words = ['i', 'am', 'feeling', 'need', 'want', 'the', 'a', 'an', 'and', 'or', 'but', 'not', 'nor', 'neither']
                key_words = [w for w in words if w not in stop_words and len(w) > 2][:3]
                search_query = " ".join(key_words) + " music" if key_words else "ambient instrumental music"
            
            # Create interpretation message
            if has_negation and detected_mood == 'neutral':
                interpretation = "Ambiguous or neutral mood detected - suggesting ambient music"
            elif has_negation:
                interpretation = f"Detected {detected_mood} mood (noting negations in your description)"
            else:
                interpretation = f"Detected {detected_mood} mood from your description"
            
            return {
                'mood_label': detected_mood,
                'search_query': search_query,
                'interpretation': interpretation
            }
        except Exception as e:
            print(f"Public interpretation error: {e}")
            return {
                'mood_label': mood_description.lower(),
                'search_query': f"{mood_description} music",
                'interpretation': mood_description
            }
    
    def _interpret_with_gemini(self, mood_description: str) -> Dict[str, str]:
        """Use Google Gemini API (free tier)"""
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.gemini_key)
            
            model = genai.GenerativeModel('gemini-pro')
            
            prompt = f"""You are a music recommendation assistant. A user described their mood as: "{mood_description}"

IMPORTANT: Pay careful attention to negations (not, nor, neither, etc.). If the user says "not happy", they are NOT happy. If they say "not happy, not sad, nor neutral", they are describing an ambiguous or complex emotional state.

Based on this description, generate:
1. A concise mood label (1-2 words, e.g., "happy", "melancholic", "energetic", "neutral", "ambiguous")
2. An optimized YouTube music search query (3-5 words that will find relevant music)
3. A brief interpretation that accurately reflects what the user said

Respond in JSON format only:
{{"mood_label": "concise mood label", "search_query": "optimized search query for YouTube", "interpretation": "brief interpretation"}}

Example for "not happy, not sad, nor neutral":
{{"mood_label": "ambiguous", "search_query": "ambient instrumental background music", "interpretation": "Ambiguous emotional state - suggesting neutral ambient music"}}"""

            response = model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.startswith("```"):
                result_text = result_text[3:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
            result_text = result_text.strip()
            
            result = json.loads(result_text)
            return result
            
        except Exception as e:
            print(f"Gemini API error: {e}")
            # Raise exception so caller can handle fallback
            raise
    
    def get_search_query(self, mood_description: str, use_llm: bool = True) -> Dict[str, str]:
        """Get search query for YouTube based on mood description"""
        # Normalize mood description for storage
        mood_normalized = mood_description.lower().strip()
        
        # Check if we have successful queries for similar moods
        if mood_normalized in self.preferences['refined_keywords']:
            successful_queries = self.preferences['refined_keywords'][mood_normalized].get('successful_queries', [])
            if successful_queries:
                return {
                    'mood_label': mood_normalized,
                    'search_query': random.choice(successful_queries),
                    'interpretation': mood_description
                }
        
        # Use LLM to interpret mood and generate query
        if use_llm:
            return self.interpret_mood_with_llm(mood_description)
        else:
            # Simple fallback
            return {
                'mood_label': mood_normalized,
                'search_query': f"{mood_description} music",
                'interpretation': mood_description
            }
    
    def search_youtube(self, query: str, max_results: int = 5, mood_normalized: str = None, genre: str = None, industry: str = None) -> List[Dict]:
        """Search YouTube for music videos"""
        if not self.api_key:
            return []
        
        # Add genre to query if specified
        if genre and genre != 'any':
            query = f"{query} {genre} music"
        
        # Add industry (Bollywood/Hollywood) to query if specified
        if industry and industry != 'any':
            if industry == 'bollywood':
                query = f"{query} bollywood"
            elif industry == 'hollywood':
                query = f"{query} hollywood"
        
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            'part': 'snippet',
            'q': query,
            'type': 'video',
            'maxResults': max_results * 2,  # Get more to filter out disliked videos
            'key': self.api_key,
            'videoCategoryId': '10'  # Music category
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            videos = []
            disliked_video_ids = set()
            
            # Get list of disliked videos for this mood to avoid showing them
            if mood_normalized and mood_normalized in self.preferences['refined_keywords']:
                disliked_videos = self.preferences['refined_keywords'][mood_normalized].get('disliked_videos', [])
                disliked_video_ids = {v.get('video_id') for v in disliked_videos if v.get('video_id')}
            
            for item in data.get('items', []):
                video_id = item['id']['videoId']
                
                # Skip disliked videos
                if video_id in disliked_video_ids:
                    continue
                
                videos.append({
                    'title': item['snippet']['title'],
                    'video_id': video_id,
                    'url': f"https://www.youtube.com/watch?v={video_id}",
                    'thumbnail': item['snippet']['thumbnails']['default']['url'],
                    'channel': item['snippet']['channelTitle']
                })
                
                # Stop when we have enough videos
                if len(videos) >= max_results:
                    break
            
            return videos
        except requests.exceptions.RequestException as e:
            print(f"Error searching YouTube: {e}")
            return []

# Initialize the app
music_app = MoodMusicApp()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search_music():
    """API endpoint to search for music based on mood description"""
    data = request.json
    mood_description = data.get('mood_description', '').strip()
    genre = data.get('genre', 'any')  # Get genre preference
    industry = data.get('industry', 'any')  # Get industry preference (Bollywood/Hollywood)
    
    if not mood_description:
        return jsonify({'error': 'Please describe your mood'}), 400
    
    # Record mood in history
    music_app.preferences['mood_history'].append({
        'mood': mood_description,
        'genre': genre,
        'industry': industry,
        'timestamp': datetime.now().isoformat()
    })
    
    # Get search query using LLM
    mood_info = music_app.get_search_query(mood_description, use_llm=True)
    search_query = mood_info['search_query']
    mood_normalized = mood_description.lower().strip()
    
    # Search YouTube (filter out disliked videos, with genre and industry preference)
    videos = music_app.search_youtube(search_query, mood_normalized=mood_normalized, genre=genre, industry=industry)
    
    if not videos:
        return jsonify({'error': 'No videos found. Please check your API key or try a different mood description.'}), 500
    
    return jsonify({
        'mood_description': mood_description,
        'mood_label': mood_info.get('mood_label', mood_description),
        'interpretation': mood_info.get('interpretation', mood_description),
        'query': search_query,
        'videos': videos
    })

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """API endpoint to submit feedback"""
    data = request.json
    mood_description = data.get('mood_description', '')
    feedback = data.get('feedback', '')
    query = data.get('query', '')
    video_id = data.get('video_id', '')
    video_title = data.get('video_title', '')
    
    if mood_description and feedback and query:
        music_app.refine_keywords(mood_description, feedback, query, video_id, video_title)
        music_app.save_preferences()
        return jsonify({'success': True, 'message': 'Feedback recorded!'})
    
    return jsonify({'error': 'Invalid feedback data'}), 400

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎵 Mood Music App - Web Version")
    print("="*60)
    print("\nStarting server...")
    print("📍 Local URL: http://localhost:5000")
    print("📍 Alternative: http://127.0.0.1:5000")
    print("\nPress Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

