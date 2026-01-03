"""
Shopee Data Scraper Module
"""
import json
import logging
from typing import Optional, Dict, List, Any
from tls_client_wrapper import TLSClientWrapper
from config import Config

logger = logging.getLogger(__name__)


class ShopeeDataScraper:
    """Scraper for collecting data from Shopee Vietnam"""
    
    def __init__(self):
        """Initialize Shopee scraper with TLS client"""
        self.client = TLSClientWrapper()
        self.base_url = Config.SHOPEE_VN_URL
        logger.info("ShopeeDataScraper initialized")
    
    def get_homepage_data(self) -> Optional[Dict[str, Any]]:
        """
        Fetch homepage data from Shopee
        
        Returns:
            Dictionary containing homepage data or None if failed
        """
        try:
            response = self.client.get(self.base_url)
            
            if response:
                return {
                    'status_code': response.status_code,
                    'url': response.url,
                    'content_length': len(response.text),
                    'headers': dict(response.headers),
                    'success': True
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error fetching homepage data: {str(e)}")
            return None
    
    def search_products(self, keyword: str, limit: int = 10) -> Optional[List[Dict[str, Any]]]:
        """
        Search for products on Shopee
        
        Args:
            keyword: Search keyword (will be URL-encoded by the HTTP client)
            limit: Maximum number of results (must be positive, max 100)
            
        Returns:
            List of product data or None if failed
        """
        # Validate inputs
        if not keyword or not keyword.strip():
            logger.error("Keyword cannot be empty")
            return None
        
        if not isinstance(limit, int) or limit <= 0:
            logger.error(f"Invalid limit value: {limit}. Must be a positive integer")
            return None
        
        if limit > 100:
            logger.error(f"Limit {limit} exceeds maximum allowed value of 100")
            return None
        
        try:
            # Shopee API endpoint for search (example)
            search_url = f"{self.base_url}api/v4/search/search_items"
            params = {
                'keyword': keyword.strip(),
                'limit': limit,
                'newest': 0,
                'order': 'desc',
                'page_type': 'search',
                'scenario': 'PAGE_GLOBAL_SEARCH',
                'version': 2
            }
            
            response = self.client.get(search_url, params=params)
            
            if response:
                try:
                    data = response.json()
                    return data
                except json.JSONDecodeError:
                    logger.warning("Failed to parse JSON response")
                    return None
            
            return None
            
        except Exception as e:
            logger.error(f"Error searching products: {str(e)}")
            return None
    
    def get_product_details(self, shop_id: int, item_id: int) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific product
        
        Args:
            shop_id: Shop ID (must be a positive integer)
            item_id: Product/Item ID (must be a positive integer)
            
        Returns:
            Product details or None if failed
        """
        # Validate inputs
        if not isinstance(shop_id, int) or shop_id <= 0:
            logger.error(f"Invalid shop_id: {shop_id}. Must be a positive integer")
            return None
        
        if not isinstance(item_id, int) or item_id <= 0:
            logger.error(f"Invalid item_id: {item_id}. Must be a positive integer")
            return None
        
        try:
            # Shopee API endpoint for product details (example)
            detail_url = f"{self.base_url}api/v4/item/get"
            params = {
                'shopid': shop_id,
                'itemid': item_id
            }
            
            response = self.client.get(detail_url, params=params)
            
            if response:
                try:
                    data = response.json()
                    return data
                except json.JSONDecodeError:
                    logger.warning("Failed to parse JSON response")
                    return None
            
            return None
            
        except Exception as e:
            logger.error(f"Error fetching product details: {str(e)}")
            return None
    
    def close(self):
        """Close the scraper and cleanup resources"""
        self.client.close()
        logger.info("ShopeeDataScraper closed")
