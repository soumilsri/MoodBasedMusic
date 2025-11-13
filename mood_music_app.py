#!/usr/bin/env python3
"""
Mood Music App - Plays music based on user mood with feedback loop
"""

import os
import json
import random
import requests
from typing import Dict, List, Optional
from dotenv import load_dotenv
from colorama import init, Fore, Style
from datetime import datetime

# Initialize colorama for Windows
init(autoreset=True)

# Load environment variables
load_dotenv()

class MoodMusicApp:
    def __init__(self):
        self.api_key = os.getenv('YOUTUBE_API_KEY')
        self.preferences_file = 'user_preferences.json'
        self.preferences = self.load_preferences()
        
        # Mood to music mapping with initial keywords
        self.mood_keywords = {
            'happy': ['upbeat', 'energetic', 'joyful', 'celebratory'],
            'sad': ['melancholic', 'emotional', 'calm', 'reflective'],
            'energetic': ['high energy', 'intense', 'powerful', 'motivational'],
            'relaxed': ['ambient', 'chill', 'peaceful', 'meditation'],
            'focused': ['instrumental', 'concentration', 'study music', 'lo-fi'],
            'romantic': ['love songs', 'romantic', 'soft', 'intimate'],
            'angry': ['aggressive', 'intense', 'powerful', 'heavy'],
            'nostalgic': ['classic', 'retro', 'vintage', 'oldies']
        }
        
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
    
    def get_user_mood(self) -> str:
        """Get mood input from user"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}Welcome to Mood Music App!")
        print(f"{Fore.CYAN}{'='*60}\n")
        
        print(f"{Fore.YELLOW}How are you feeling today?")
        print(f"{Fore.WHITE}Available moods:")
        
        moods = list(self.mood_keywords.keys())
        for i, mood in enumerate(moods, 1):
            print(f"  {Fore.GREEN}{i}. {mood.capitalize()}")
        
        while True:
            try:
                choice = input(f"\n{Fore.CYAN}Enter mood number or name: ").strip().lower()
                
                # Check if it's a number
                if choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(moods):
                        return moods[idx]
                
                # Check if it's a mood name
                if choice in moods:
                    return choice
                
                print(f"{Fore.RED}Invalid choice. Please try again.")
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Goodbye!")
                exit(0)
    
    def refine_keywords(self, mood: str, feedback: str, query: str):
        """Refine keywords based on user feedback"""
        if mood not in self.preferences['refined_keywords']:
            self.preferences['refined_keywords'][mood] = {
                'liked_keywords': [],
                'disliked_keywords': [],
                'successful_queries': []
            }
        
        # Store feedback for learning
        feedback_entry = {
            'mood': mood,
            'feedback': feedback,
            'query': query,
            'timestamp': datetime.now().isoformat()
        }
        self.preferences['feedback_history'].append(feedback_entry)
        
        # Learn from feedback
        if feedback == 'like':
            # Extract keywords from successful query
            query_words = query.lower().split()
            # Add successful query to liked keywords
            if query not in self.preferences['refined_keywords'][mood]['successful_queries']:
                self.preferences['refined_keywords'][mood]['successful_queries'].append(query)
        elif feedback == 'dislike':
            # Track what didn't work (simplified - could be enhanced)
            pass
    
    def get_search_query(self, mood: str) -> str:
        """Get search query for YouTube based on mood and preferences"""
        # Check if we have successful queries for this mood
        if mood in self.preferences['refined_keywords']:
            successful_queries = self.preferences['refined_keywords'][mood].get('successful_queries', [])
            if successful_queries:
                # Use a successful query from history (rotate through them)
                return random.choice(successful_queries)
        
        # Start with base keywords
        keywords = self.mood_keywords[mood].copy()
        
        # Use the first keyword as primary, add mood name
        query = f"{mood} {keywords[0]} music"
        return query
    
    def search_youtube(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search YouTube for music videos"""
        if not self.api_key:
            print(f"{Fore.RED}Error: YouTube API key not found!")
            print(f"{Fore.YELLOW}Please set YOUTUBE_API_KEY in .env file")
            print(f"{Fore.YELLOW}You can still see the app structure, but YouTube search won't work without an API key.")
            return []
        
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            'part': 'snippet',
            'q': query,
            'type': 'video',
            'maxResults': max_results,
            'key': self.api_key,
            'videoCategoryId': '10'  # Music category
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            videos = []
            for item in data.get('items', []):
                videos.append({
                    'title': item['snippet']['title'],
                    'video_id': item['id']['videoId'],
                    'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                    'thumbnail': item['snippet']['thumbnails']['default']['url']
                })
            
            return videos
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}Error searching YouTube: {e}")
            return []
    
    def display_results(self, videos: List[Dict], mood: str):
        """Display search results to user"""
        if not videos:
            print(f"{Fore.RED}No videos found. Try a different mood!")
            return None
        
        print(f"\n{Fore.GREEN}{'='*60}")
        print(f"{Fore.GREEN}Here are some {mood} music suggestions:")
        print(f"{Fore.GREEN}{'='*60}\n")
        
        for i, video in enumerate(videos, 1):
            print(f"{Fore.CYAN}{i}. {Fore.WHITE}{video['title']}")
            print(f"   {Fore.YELLOW}URL: {video['url']}\n")
        
        return videos
    
    def get_feedback(self, mood: str) -> str:
        """Get user feedback on the suggestions"""
        print(f"\n{Fore.CYAN}How do you like these suggestions?")
        print(f"{Fore.WHITE}1. Like - I'll remember this preference")
        print(f"{Fore.WHITE}2. Dislike - I'll adjust for next time")
        print(f"{Fore.WHITE}3. Skip - No feedback")
        
        while True:
            choice = input(f"\n{Fore.CYAN}Enter your choice (1-3): ").strip()
            
            if choice == '1':
                return 'like'
            elif choice == '2':
                return 'dislike'
            elif choice == '3':
                return 'skip'
            else:
                print(f"{Fore.RED}Invalid choice. Please enter 1, 2, or 3.")
    
    def run(self):
        """Main application loop"""
        try:
            while True:
                # Get user mood
                mood = self.get_user_mood()
                
                # Record mood in history
                self.preferences['mood_history'].append({
                    'mood': mood,
                    'timestamp': datetime.now().isoformat()
                })
                
                # Get search query based on mood and preferences
                query = self.get_search_query(mood)
                print(f"\n{Fore.YELLOW}Searching for: {query}...")
                
                # Search YouTube
                videos = self.search_youtube(query)
                
                # Display results
                displayed_videos = self.display_results(videos, mood)
                
                if displayed_videos:
                    # Get feedback
                    feedback = self.get_feedback(mood)
                    
                    if feedback != 'skip':
                        # Refine keywords based on feedback
                        self.refine_keywords(mood, feedback, query)
                        print(f"{Fore.GREEN}Thank you for your feedback! I'll remember your preference.")
                    
                    # Save preferences
                    self.save_preferences()
                
                # Ask if user wants to continue
                print(f"\n{Fore.CYAN}{'='*60}")
                continue_choice = input(f"{Fore.CYAN}Would you like to search for more music? (y/n): ").strip().lower()
                
                if continue_choice != 'y':
                    print(f"{Fore.YELLOW}Thanks for using Mood Music App! Goodbye!")
                    break
                
                print()
        
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Goodbye!")
        except Exception as e:
            print(f"{Fore.RED}An error occurred: {e}")

if __name__ == "__main__":
    app = MoodMusicApp()
    app.run()

