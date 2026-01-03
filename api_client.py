"""
API Client for invoking internal APIs
"""
import json
import logging
from typing import Optional, Dict, Any
from tls_client_wrapper import TLSClientWrapper
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InternalAPIClient:
    """Client for interacting with internal APIs"""
    
    def __init__(self, api_url: str = None):
        """
        Initialize API client
        
        Args:
            api_url: Base URL for internal API (defaults to Config.INTERNAL_API_URL)
        """
        self.client = TLSClientWrapper()
        self.api_url = api_url or Config.INTERNAL_API_URL
        logger.info(f"InternalAPIClient initialized with URL: {self.api_url}")
    
    def send_data(self, endpoint: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Send data to internal API
        
        Args:
            endpoint: API endpoint path (e.g., '/data', '/products')
            data: Data to send
            
        Returns:
            API response or None if failed
        """
        try:
            url = f"{self.api_url.rstrip('/')}/{endpoint.lstrip('/')}"
            logger.info(f"Sending data to internal API: {url}")
            
            response = self.client.post(url, json_data=data)
            
            if response:
                try:
                    result = response.json()
                    logger.info("Successfully sent data to internal API")
                    return result
                except json.JSONDecodeError:
                    logger.warning("Response is not JSON format")
                    return {
                        'status_code': response.status_code,
                        'text': response.text,
                        'success': True
                    }
            
            return None
            
        except Exception as e:
            logger.error(f"Error sending data to API: {str(e)}")
            return None
    
    def get_data(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict[str, Any]]:
        """
        Retrieve data from internal API
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            
        Returns:
            API response or None if failed
        """
        try:
            url = f"{self.api_url.rstrip('/')}/{endpoint.lstrip('/')}"
            logger.info(f"Getting data from internal API: {url}")
            
            response = self.client.get(url, params=params)
            
            if response:
                try:
                    result = response.json()
                    logger.info("Successfully retrieved data from internal API")
                    return result
                except json.JSONDecodeError:
                    logger.warning("Response is not JSON format")
                    return {
                        'status_code': response.status_code,
                        'text': response.text,
                        'success': True
                    }
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting data from API: {str(e)}")
            return None
    
    def close(self):
        """Close the API client"""
        self.client.close()
        logger.info("InternalAPIClient closed")
