# utils/api_handler.py
import time
import logging
import google.generativeai as genai
from typing import Optional
from config.settings import Config

logger = logging.getLogger(__name__)

class RateLimitedGeminiHandler:
    """Handler for Gemini API calls with rate limiting"""
    
    def __init__(self, model_name: str = 'gemini-1.5-flash', max_retries: int = 3):
        self.model_name = model_name
        self.max_retries = max_retries
        self.last_request_time = 0
        self.min_request_interval = 1  # 1 second between requests
        
        # Initialize Gemini
        config = Config()
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(model_name)
    
    def generate_content_with_retry(self, prompt: str, **kwargs) -> Optional[str]:
        """Generate content with rate limiting and retry logic"""
        
        for attempt in range(self.max_retries):
            try:
                # Rate limiting
                current_time = time.time()
                time_since_last = current_time - self.last_request_time
                
                if time_since_last < self.min_request_interval:
                    sleep_time = self.min_request_interval - time_since_last
                    logger.info(f"Rate limiting: waiting {sleep_time:.2f} seconds")
                    time.sleep(sleep_time)
                
                # Configure for free tier
                generation_config = genai.types.GenerationConfig(
                    temperature=0.3,
                    top_p=0.8,
                    max_output_tokens=2048,  # Conservative for free tier
                    **kwargs
                )
                
                logger.info(f"Sending request to {self.model_name} (attempt {attempt + 1})")
                response = self.model.generate_content(prompt, generation_config=generation_config)
                
                self.last_request_time = time.time()
                
                if response and response.text:
                    logger.info(f"Successfully received response")
                    return response.text.strip()
                else:
                    logger.warning("Empty response received")
                    
            except Exception as e:
                error_str = str(e)
                logger.error(f"Attempt {attempt + 1} failed: {error_str}")
                
                if "429" in error_str or "quota" in error_str.lower():
                    sleep_time = min(30 * (attempt + 1), 120)  # Max 2 minutes
                    logger.warning(f"Rate limit hit. Waiting {sleep_time} seconds...")
                    time.sleep(sleep_time)
                    self.min_request_interval = max(self.min_request_interval * 1.5, 3)
                elif attempt == self.max_retries - 1:
                    raise e
                else:
                    time.sleep(2)
        
        return None

# Global handler
gemini_handler = RateLimitedGeminiHandler()
