import requests
import json
from typing import List, Dict, Any, Optional

class GeminiAPI:
    """Class to interact with Google's Gemini API for news enhancement"""
    
    # API configuration
    BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"
    
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-pro"):
        """Initialize the Gemini API client
        
        Args:
            api_key: Google API key for Gemini
            model_name: Gemini model to use (default: gemini-1.5-pro)
        """
        self.api_key = api_key
        self.model_name = model_name
    
    def generate_content(self, prompt: str) -> Dict[str, Any]:
        """Send a prompt to the Gemini API and get a response
        
        Args:
            prompt: Text prompt to send to the model
            
        Returns:
            Dictionary containing the API response
        """
        url = f"{self.BASE_URL}/{self.model_name}:generateContent?key={self.api_key}"
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()  # Raise exception for HTTP errors
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def summarize_article(self, article_title: str, article_content: str) -> str:
        """Generate a concise summary of a news article
        
        Args:
            article_title: Title of the news article
            article_content: Content/body of the news article
            
        Returns:
            Summarized version of the article
        """
        prompt = f"""Summarize the following news article in 3-4 sentences:
        
Title: {article_title}

Content: {article_content}

Summary:"""
        
        response = self.generate_content(prompt)
        
        # Extract the summary from the response
        try:
            summary = response["candidates"][0]["content"]["parts"][0]["text"]
            return summary
        except (KeyError, IndexError):
            return "Unable to generate summary."
    
    def generate_insights(self, headlines: List[Dict[str, str]]) -> Dict[str, Any]:
        """Generate insights from a collection of news headlines
        
        Args:
            headlines: List of headline dictionaries with 'title' and 'source' keys
            
        Returns:
            Dictionary with insights including trends and recommendations
        """
        # Format headlines for the prompt
        headlines_text = "\n".join([f"- {h['title']} (Source: {h['source']})" for h in headlines])
        
        prompt = f"""Analyze these news headlines and provide insights:
        
{headlines_text}

Please provide:
1. Top 3 trending topics
2. Key insights about these headlines
3. Recommended articles to read first

IMPORTANT: Format your response without using asterisks (*) for bullet points. Use proper headings and paragraphs instead."""
        
        response = self.generate_content(prompt)
        
        # Extract the insights from the response
        try:
            insights_text = response["candidates"][0]["content"]["parts"][0]["text"]
            return {
                "success": True,
                "insights": insights_text
            }
        except (KeyError, IndexError):
            return {
                "success": False,
                "error": "Unable to generate insights."
            }
    
    def personalize_recommendations(self, user_interests: List[str], headlines: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Generate personalized news recommendations based on user interests
        
        Args:
            user_interests: List of topics/categories the user is interested in
            headlines: List of headline dictionaries with 'title', 'url', and 'source' keys
            
        Returns:
            List of recommended headlines sorted by relevance to user interests
        """
        # Format inputs for the prompt
        interests_text = ", ".join(user_interests)
        headlines_text = "\n".join([f"- {h['title']} (Source: {h['source']})" for h in headlines])
        
        prompt = f"""Given a user interested in {interests_text}, rank the following news headlines from most to least relevant:
        
{headlines_text}

Return only the titles of the top 5 most relevant articles in order of relevance. Do not use asterisks (*) in your response. Use numbers (1, 2, 3...) instead."""
        
        response = self.generate_content(prompt)
        
        # Extract recommended headlines
        try:
            recommendations_text = response["candidates"][0]["content"]["parts"][0]["text"]
            # Clean up the response - remove asterisks and other bullet point markers
            recommended_titles = [line.strip().replace('- ', '').replace('* ', '').replace('• ', '') for line in recommendations_text.split('\n') if line.strip()]
            # Also remove any numeric prefixes like "1. ", "2. ", etc.
            recommended_titles = [title.strip() if not title.strip()[0].isdigit() else title.strip()[title.find('.')+1:].strip() for title in recommended_titles]
            
            # Match recommended titles with original headline data
            recommended_headlines = []
            for title in recommended_titles:
                for headline in headlines:
                    # Find the closest matching headline
                    if title.lower() in headline['title'].lower() or headline['title'].lower() in title.lower():
                        recommended_headlines.append(headline)
                        break
            
            return recommended_headlines
        except (KeyError, IndexError):
            # Return original headlines if recommendation fails
            return headlines[:5] if len(headlines) > 5 else headlines