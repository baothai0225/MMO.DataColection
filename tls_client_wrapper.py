"""
TLS Client Wrapper for accessing websites with enhanced security
"""
import time
import logging
from typing import Optional, Dict
import tls_client
from config import Config

logger = logging.getLogger(__name__)


class TLSClientWrapper:
    """Wrapper class for tls_client to handle website access"""
    
    def __init__(self, client_identifier: str = None):
        """
        Initialize TLS client
        
        Args:
            client_identifier: Browser identifier for TLS client (e.g., 'chrome_120')
        """
        self.client_identifier = client_identifier or Config.TLS_CLIENT_IDENTIFIER
        self.session = tls_client.Session(client_identifier=self.client_identifier)
        self.session.headers.update(Config.get_headers())
        logger.info(f"TLS Client initialized with identifier: {self.client_identifier}")
    
    def get(self, url: str, params: Optional[Dict] = None, max_retries: int = None, timeout: int = None) -> Optional[tls_client.response.Response]:
        """
        Perform GET request with retry logic
        
        Args:
            url: Target URL
            params: Query parameters
            max_retries: Maximum number of retries (defaults to Config.MAX_RETRIES)
            timeout: Request timeout in seconds (defaults to Config.API_TIMEOUT)
            
        Returns:
            Response object or None if failed
        """
        max_retries = max_retries or Config.MAX_RETRIES
        timeout = timeout or Config.API_TIMEOUT
        
        for attempt in range(max_retries):
            try:
                logger.info(f"GET request to {url} (attempt {attempt + 1}/{max_retries})")
                response = self.session.get(url, params=params, timeout=timeout)
                
                if response.status_code == 200:
                    logger.info(f"Successfully retrieved data from {url}")
                    return response
                else:
                    logger.warning(f"Request failed with status code: {response.status_code}")
                    
            except tls_client.exceptions.TLSClientExeption as e:
                logger.error(f"TLS client error during GET request: {str(e)}")
            except Exception as e:
                logger.error(f"Unexpected error during GET request: {str(e)}")
                
            if attempt < max_retries - 1:
                delay = Config.RETRY_DELAY * (2 ** attempt)  # Exponential backoff
                logger.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
        
        logger.error(f"Failed to retrieve data from {url} after {max_retries} attempts")
        return None
    
    def post(self, url: str, data: Optional[Dict] = None, json_data: Optional[Dict] = None, 
             max_retries: int = None, timeout: int = None) -> Optional[tls_client.response.Response]:
        """
        Perform POST request with retry logic
        
        Args:
            url: Target URL
            data: Form data
            json_data: JSON data
            max_retries: Maximum number of retries
            timeout: Request timeout in seconds (defaults to Config.API_TIMEOUT)
            
        Returns:
            Response object or None if failed
        """
        max_retries = max_retries or Config.MAX_RETRIES
        timeout = timeout or Config.API_TIMEOUT
        
        for attempt in range(max_retries):
            try:
                logger.info(f"POST request to {url} (attempt {attempt + 1}/{max_retries})")
                response = self.session.post(url, data=data, json=json_data, timeout=timeout)
                
                if response.status_code in [200, 201]:
                    logger.info(f"Successfully posted data to {url}")
                    return response
                else:
                    logger.warning(f"Request failed with status code: {response.status_code}")
                    
            except tls_client.exceptions.TLSClientExeption as e:
                logger.error(f"TLS client error during POST request: {str(e)}")
            except Exception as e:
                logger.error(f"Unexpected error during POST request: {str(e)}")
                
            if attempt < max_retries - 1:
                delay = Config.RETRY_DELAY * (2 ** attempt)  # Exponential backoff
                logger.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
        
        logger.error(f"Failed to post data to {url} after {max_retries} attempts")
        return None
    
    def close(self):
        """Close the TLS client session"""
        if hasattr(self.session, 'close'):
            self.session.close()
        logger.info("TLS Client session closed")
