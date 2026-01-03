"""
API Client for invoking internal APIs
"""
import json
import logging
import re
from typing import Optional, Dict, Any
from tls_client_wrapper import TLSClientWrapper
from config import Config

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
        # Validate endpoint
        if not self._validate_endpoint(endpoint):
            logger.error(f"Invalid endpoint: {endpoint}")
            return None
        
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
                        'json_parsed': False
                    }
            
            return None
            
        except Exception as e:
            logger.error(f"Error sending data to API: {str(e)}")
            return None
    
    def _validate_endpoint(self, endpoint: str) -> bool:
        """
        Validate endpoint to prevent path traversal and other security issues
        
        Args:
            endpoint: Endpoint to validate
            
        Returns:
            True if endpoint is valid, False otherwise
        """
        if not endpoint:
            return False
        
        # Check for path traversal attempts
        if '..' in endpoint or '\\' in endpoint:
            return False
        
        # Check for valid characters (alphanumeric, dash, underscore, slash)
        if not re.match(r'^[a-zA-Z0-9/_-]+$', endpoint.strip('/')):
            return False
        
        return True
    
    def get_data(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict[str, Any]]:
        """
        Retrieve data from internal API
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            
        Returns:
            API response or None if failed
        """
        # Validate endpoint
        if not self._validate_endpoint(endpoint):
            logger.error(f"Invalid endpoint: {endpoint}")
            return None
        
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
                        'json_parsed': False
                    }
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting data from API: {str(e)}")
            return None
    
    def close(self):
        """Close the API client"""
        self.client.close()
        logger.info("InternalAPIClient closed")
