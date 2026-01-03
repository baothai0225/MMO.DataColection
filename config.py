"""
Configuration module for the data collection project
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for the data collection project"""
    
    # API Configuration
    INTERNAL_API_URL = os.getenv('INTERNAL_API_URL', 'http://localhost:8000/api')
    API_TIMEOUT = int(os.getenv('API_TIMEOUT', '30'))
    
    # TLS Client Configuration
    TLS_CLIENT_IDENTIFIER = os.getenv('TLS_CLIENT_IDENTIFIER', 'chrome_120')
    USER_AGENT = os.getenv('USER_AGENT', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    # Data Collection Settings
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))
    RETRY_DELAY = int(os.getenv('RETRY_DELAY', '2'))
    
    # Target Websites
    SHOPEE_VN_URL = 'https://shopee.vn/'
    
    @classmethod
    def get_headers(cls):
        """Get default headers for requests"""
        return {
            'User-Agent': cls.USER_AGENT,
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
